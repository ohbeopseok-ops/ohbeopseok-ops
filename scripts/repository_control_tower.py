#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
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
    req = urllib.request.Request(
        API + path,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "joylab-repository-control-tower-v0.1",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def parse_dt(value: str | None):
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def age_days(value: str | None, now: datetime):
    dt = parse_dt(value)
    if not dt:
        return None
    return (now - dt).total_seconds() / 86400


def latest_actions(repo: str):
    q = urllib.parse.urlencode({"per_page": 10})
    data = api_get(f"/repos/{OWNER}/{repo}/actions/runs?{q}")
    runs = data.get("workflow_runs", [])
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
        for run in runs
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
    if not TOKEN:
        print("GITHUB_TOKEN is required", file=sys.stderr)
        return 2

    now = datetime.now(timezone.utc)
    repos = api_get("/user/repos?affiliation=owner&per_page=100&sort=updated")
    repos = [r for r in repos if r.get("owner", {}).get("login") == OWNER]

    rows = []
    for repo in sorted(repos, key=lambda x: x["name"].lower()):
        runs = latest_actions(repo["name"])
        state, reason = classify(repo, runs, now)
        latest = runs[0] if runs else None
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
                "latest_action": latest,
            }
        )

    counts = {}
    for row in rows:
        counts[row["state"]] = counts.get(row["state"], 0) + 1

    payload = {
        "schema_version": "1.0",
        "generated_at": now.isoformat(),
        "owner": OWNER,
        "classification": {
            "ACTIVE_DAYS": ACTIVE_DAYS,
            "STALE_DAYS": STALE_DAYS,
            "failed_conclusions": [
                "failure", "timed_out", "action_required", "startup_failure"
            ],
        },
        "counts": counts,
        "repositories": rows,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# JoyLab Repository Control Tower V0.1",
        "",
        f"Generated: {now.isoformat()}",
        "",
        "> AUTO-GENERATED. Do not manually edit this file.",
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
        action = "—"
        if latest:
            action = f"{latest.get('name')} / {latest.get('status')} / {latest.get('conclusion') or '—'}"
        reason = str(row["reason"]).replace("|", "\\|")
        lines.append(f"| {row['repository']} | **{row['state']}** | {action} | {reason} |")

    lines += [
        "",
        "## Gate policy",
        "",
        "- BROKEN has highest remediation priority.",
        "- A GREEN run is only current for its exact commit; stale historical GREEN does not certify newer code.",
        "- EMPTY repositories are not given CI work until a project payload exists.",
        "- ARCHIVE remains a governance decision; V0.1 does not archive repositories automatically.",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(counts, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
