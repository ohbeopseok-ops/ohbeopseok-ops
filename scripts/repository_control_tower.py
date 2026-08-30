#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API = "https://api.github.com"
OWNER = os.environ.get("JOYLAB_GITHUB_OWNER", "ohbeopseok-ops")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT_JSON = Path("control_tower/repository-health.json")
OUT_MD = Path("GITHUB_HEALTH_REGISTRY_AUTO.md")
ACTIVE_DAYS = 14
STALE_DAYS = 60


def api_get(path: str):
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "joylab-repository-control-tower-v0.1",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(API + path, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def discover_repos():
    try:
        repos = api_get("/user/repos?affiliation=owner&per_page=100&sort=updated")
        owned = [r for r in repos if r.get("owner", {}).get("login") == OWNER]
        return owned, "authenticated-owner-scan"
    except urllib.error.HTTPError as exc:
        if exc.code not in {401, 403, 404}:
            raise
        repos = api_get(f"/users/{OWNER}/repos?per_page=100&sort=updated")
        return repos, "public-fallback"


def parse_dt(value: str | None):
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def age_days(value: str | None, now: datetime):
    dt = parse_dt(value)
    return None if not dt else (now - dt).total_seconds() / 86400


def latest_actions(repo: str):
    q = urllib.parse.urlencode({"per_page": 10})
    data = api_get(f"/repos/{OWNER}/{repo}/actions/runs?{q}")
    return [
        {
            "id": run.get("id"),
            "name": run.get("name"),
            "event": run.get("event"),
            "status": run.get("status"),
            "conclusion": run.get("conclusion"),
            "head_sha": run.get("head_sha"),
            "created_at": run.get("created_at"),
            "html_url": run.get("html_url"),
        }
        for run in data.get("workflow_runs", [])
    ]


def classify(repo: dict, runs: list[dict], now: datetime):
    if repo.get("archived"):
        return "ARCHIVE", "repository archived"
    if repo.get("size", 0) == 0:
        return "EMPTY", "repository size is 0"

    completed = [r for r in runs if r.get("status") == "completed"]
    latest_completed = completed[0] if completed else None
    if latest_completed and latest_completed.get("conclusion") in {
        "failure", "timed_out", "action_required", "startup_failure"
    }:
        return "BROKEN", f"latest completed Actions run failed: {latest_completed.get('name')}"

    days = age_days(repo.get("pushed_at"), now)
    if days is not None and days <= ACTIVE_DAYS:
        return "ACTIVE", f"push activity within {ACTIVE_DAYS} days"
    if days is not None and days > STALE_DAYS:
        return "STALE", f"no push for more than {STALE_DAYS} days"
    return "HEALTHY", "no known blocking failure"


def main():
    now = datetime.now(timezone.utc)
    repos, scope_mode = discover_repos()

    rows = []
    for repo in sorted(repos, key=lambda x: x["name"].lower()):
        try:
            runs = latest_actions(repo["name"])
        except urllib.error.HTTPError:
            runs = []
        state, reason = classify(repo, runs, now)
        rows.append(
            {
                "repository": repo["full_name"],
                "visibility": repo.get("visibility"),
                "default_branch": repo.get("default_branch"),
                "size_kb": repo.get("size", 0),
                "archived": repo.get("archived", False),
                "pushed_at": repo.get("pushed_at"),
                "state": state,
                "reason": reason,
                "latest_action": runs[0] if runs else None,
            }
        )

    counts = {}
    for row in rows:
        counts[row["state"]] = counts.get(row["state"], 0) + 1

    payload = {
        "schema_version": "1.0",
        "generated_at": now.isoformat(),
        "owner": OWNER,
        "scope_mode": scope_mode,
        "private_repositories_included": scope_mode == "authenticated-owner-scan",
        "counts": counts,
        "repositories": rows,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# JoyLab Repository Control Tower V0.1",
        "",
        f"Generated: {now.isoformat()}",
        f"Scope: **{scope_mode}**",
        "",
        "> AUTO-GENERATED. Do not manually edit this file.",
    ]
    if scope_mode == "public-fallback":
        lines += [
            "",
            "> ⚠️ Private repositories are not included because this workflow does not have a cross-repository token. Add a repository secret named CONTROL_TOWER_TOKEN with read access to owned private repositories to enable the full scan.",
        ]

    lines += [
        "",
        "## Summary",
        "",
        "| State | Count |",
        "|---|---:|",
    ]
    for state in ["BROKEN", "ACTIVE", "HEALTHY", "STALE", "EMPTY", "ARCHIVE"]:
        lines.append(f"| {state} | {counts.get(state, 0)} |")

    lines += [
        "",
        "## Repository Health",
        "",
        "| Repository | State | Latest Actions | Reason |",
        "|---|---|---|---|",
    ]
    order = {"BROKEN": 0, "ACTIVE": 1, "HEALTHY": 2, "STALE": 3, "EMPTY": 4, "ARCHIVE": 5}
    for row in sorted(rows, key=lambda r: (order.get(r["state"], 99), r["repository"].lower())):
        latest = row["latest_action"]
        action = "—" if not latest else f"{latest.get('name')} / {latest.get('status')} / {latest.get('conclusion') or '—'}"
        reason = str(row["reason"]).replace("|", "\\|")
        lines.append(f"| {row['repository']} | **{row['state']}** | {action} | {reason} |")

    lines += [
        "",
        "## Gate policy",
        "",
        "- BROKEN has highest remediation priority.",
        "- Historical GREEN never certifies a newer commit.",
        "- EMPTY repositories do not receive synthetic CI work.",
        "- V0.1 never archives or deletes repositories automatically.",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"scope_mode": scope_mode, "counts": counts}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
