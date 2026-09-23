#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

API = "https://api.github.com"
OWNER = os.environ.get("JOYLAB_GITHUB_OWNER", "ohbeopseok-ops")
TOKEN = os.environ.get("CONTROL_TOWER_TOKEN") or os.environ.get("GITHUB_TOKEN", "")
OUT_JSON = Path("control_tower/repository-health-v0.2.json")
OUT_MD = Path("GITHUB_HEALTH_REGISTRY_V0.2.md")
GOVERNANCE_FILE = Path("control_tower/repository-governance.json")

CRITICAL_NAME_RE = re.compile(r"(release gate|\bci\b|build|test|deploy|validation|validate|hero gate)", re.I)


def api_get(path: str):
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "joylab-repository-control-tower-v0.2",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(API + path, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def paginate(path: str):
    page = 1
    items = []
    while True:
        sep = "&" if "?" in path else "?"
        batch = api_get(f"{path}{sep}per_page=100&page={page}")
        if not isinstance(batch, list):
            return batch
        items.extend(batch)
        if len(batch) < 100:
            return items
        page += 1


def discover_repos():
    try:
        repos = paginate("/user/repos?affiliation=owner&sort=updated")
        owned = [r for r in repos if r.get("owner", {}).get("login") == OWNER]
        return owned, "authenticated-owner-scan"
    except urllib.error.HTTPError as exc:
        if exc.code not in {401, 403, 404}:
            raise
        return paginate(f"/users/{OWNER}/repos?sort=updated"), "public-fallback"


def parse_dt(value):
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def age_days(value, now):
    dt = parse_dt(value)
    return None if not dt else (now - dt).total_seconds() / 86400


def latest_actions(repo: str):
    q = urllib.parse.urlencode({"per_page": 30})
    data = api_get(f"/repos/{OWNER}/{repo}/actions/runs?{q}")
    return data.get("workflow_runs", [])


def latest_per_workflow(runs):
    out = {}
    for run in runs:
        name = run.get("name") or "unnamed"
        if name not in out:
            out[name] = run
    return out


def failure_code(run):
    name = (run.get("name") or "").lower()
    if "scoring" in name or "gsc" in name or "naver" in name:
        return "DATA_PIPELINE_FAILURE"
    if "portfolio" in name or "dashboard sync" in name:
        return "OPERATIONAL_AUTOMATION_FAILURE"
    if "release gate" in name:
        return "RELEASE_GATE_FAILURE"
    if "build" in name:
        return "BUILD_FAILURE"
    if "test" in name or "ci" in name:
        return "CI_TEST_FAILURE"
    if "deploy" in name:
        return "DEPLOY_FAILURE"
    return "ACTIONS_FAILURE"


def classify(repo, governance, runs, now, active_days, stale_days, operational_failure_hours):
    name = repo["name"]
    rule = governance.get(name, {})
    portfolio = rule.get("portfolio", "Experiment")

    if portfolio == "Archive" or repo.get("archived"):
        return "ARCHIVE", "ARCHIVE_POLICY", "governance portfolio is Archive or repository is archived"
    if repo.get("size", 0) == 0:
        return "EMPTY", "EMPTY_REPOSITORY", "repository size is 0"

    latest = latest_per_workflow(runs)
    critical_names = set(rule.get("critical_workflows", []))
    operational_names = set(rule.get("operational_workflows", []))

    critical_failures = []
    operational_failures = []
    other_failures = []

    cutoff = now - timedelta(hours=operational_failure_hours)
    for wf_name, run in latest.items():
        if run.get("status") != "completed":
            continue
        conclusion = run.get("conclusion")
        if conclusion not in {"failure", "timed_out", "action_required", "startup_failure"}:
            continue
        created = parse_dt(run.get("created_at"))
        is_recent = not created or created >= cutoff

        if wf_name in critical_names or (not critical_names and CRITICAL_NAME_RE.search(wf_name)):
            critical_failures.append(run)
        elif wf_name in operational_names or is_recent:
            operational_failures.append(run)
        else:
            other_failures.append(run)

    if critical_failures:
        run = critical_failures[0]
        return "RED", failure_code(run), f"critical workflow failed: {run.get('name')}"
    if operational_failures:
        run = operational_failures[0]
        return "YELLOW", failure_code(run), f"operational workflow needs attention: {run.get('name')}"

    days = age_days(repo.get("pushed_at"), now)
    if days is not None and days > stale_days:
        return "STALE", "NO_RECENT_PUSH", f"no push for more than {stale_days} days"
    if days is not None and days <= active_days:
        return "GREEN", "ACTIVE_AND_CLEAR", f"push activity within {active_days} days and no blocking workflow failure"
    return "GREEN", "NO_KNOWN_BLOCKER", "no known blocking failure in latest workflow state"


def load_governance():
    return json.loads(GOVERNANCE_FILE.read_text(encoding="utf-8"))


def main():
    now = datetime.now(timezone.utc)
    governance_doc = load_governance()
    policy = governance_doc["policy"]
    governance = governance_doc["repositories"]

    repos, scope_mode = discover_repos()
    rows = []

    discovered_names = {r["name"] for r in repos}
    governed_names = set(governance)
    missing_from_scan = sorted(governed_names - discovered_names)
    ungoverned = sorted(discovered_names - governed_names)

    for repo in sorted(repos, key=lambda x: x["name"].lower()):
        try:
            runs = latest_actions(repo["name"])
        except urllib.error.HTTPError:
            runs = []

        state, code, reason = classify(
            repo,
            governance,
            runs,
            now,
            policy["active_days"],
            policy["stale_days"],
            policy["operational_failure_hours"],
        )
        latest = latest_per_workflow(runs)
        rule = governance.get(repo["name"], {})

        rows.append({
            "repository": repo["full_name"],
            "portfolio": rule.get("portfolio", "Experiment"),
            "business_owner": rule.get("owner", "UNASSIGNED"),
            "purpose": rule.get("purpose", ""),
            "visibility": repo.get("visibility"),
            "default_branch": repo.get("default_branch"),
            "size_kb": repo.get("size", 0),
            "archived": repo.get("archived", False),
            "pushed_at": repo.get("pushed_at"),
            "state": state,
            "code": code,
            "reason": reason,
            "workflow_state": {
                name: {
                    "status": run.get("status"),
                    "conclusion": run.get("conclusion"),
                    "event": run.get("event"),
                    "head_sha": run.get("head_sha"),
                    "created_at": run.get("created_at"),
                    "html_url": run.get("html_url"),
                }
                for name, run in latest.items()
            },
        })

    counts = Counter(row["state"] for row in rows)
    portfolios = Counter(row["portfolio"] for row in rows)

    payload = {
        "schema_version": "2.0",
        "generated_at": now.isoformat(),
        "owner": OWNER,
        "scope_mode": scope_mode,
        "private_repositories_included": scope_mode == "authenticated-owner-scan",
        "scan_complete": not missing_from_scan and not ungoverned and scope_mode == "authenticated-owner-scan",
        "counts": dict(counts),
        "portfolio_counts": dict(portfolios),
        "missing_from_scan": missing_from_scan,
        "ungoverned_repositories": ungoverned,
        "repositories": rows,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# JoyLab Repository Control Tower V0.2",
        "",
        f"Generated: {now.isoformat()}",
        f"Scope: **{scope_mode}**",
        f"Full scan: **{'YES' if payload['scan_complete'] else 'NO'}**",
        "",
        "> AUTO-GENERATED. Source of truth for portfolio ownership is control_tower/repository-governance.json.",
    ]
    if scope_mode != "authenticated-owner-scan":
        lines += [
            "",
            "> ⚠️ Private repositories are not included. Configure CONTROL_TOWER_TOKEN with read access to all owned repositories to activate the intended 44-repository scan.",
        ]
    if missing_from_scan:
        lines += ["", f"> Missing governed repositories from this scan: {', '.join(missing_from_scan)}"]
    if ungoverned:
        lines += ["", f"> Ungoverned repositories discovered: {', '.join(ungoverned)}"]

    lines += [
        "",
        "## Health Summary",
        "",
        "| State | Count |",
        "|---|---:|",
    ]
    for state in ["RED", "YELLOW", "GREEN", "STALE", "EMPTY", "ARCHIVE"]:
        lines.append(f"| {state} | {counts.get(state, 0)} |")

    lines += [
        "",
        "## Portfolio Summary",
        "",
        "| Portfolio | Count |",
        "|---|---:|",
    ]
    for portfolio in ["Core", "Product", "Experiment", "Reference", "Archive"]:
        lines.append(f"| {portfolio} | {portfolios.get(portfolio, 0)} |")

    lines += [
        "",
        "## Repository Health",
        "",
        "| Repository | Portfolio | State | Code | Reason |",
        "|---|---|---|---|---|",
    ]
    order = {"RED": 0, "YELLOW": 1, "GREEN": 2, "STALE": 3, "EMPTY": 4, "ARCHIVE": 5}
    for row in sorted(rows, key=lambda r: (order.get(r["state"], 99), r["repository"].lower())):
        reason = str(row["reason"]).replace("|", "\\|")
        lines.append(
            f"| {row['repository']} | {row['portfolio']} | **{row['state']}** | {row['code']} | {reason} |"
        )

    lines += [
        "",
        "## V0.2 policy",
        "",
        "- RED: latest critical workflow failed.",
        "- YELLOW: recent operational automation failed but release/CI critical gates are not known broken.",
        "- GREEN: no current blocker and repository is not stale/empty/archive.",
        f"- STALE: no push for more than {policy['stale_days']} days.",
        "- EMPTY: repository contains no committed project payload.",
        "- ARCHIVE: governance explicitly classifies the repository as Archive, or GitHub marks it archived.",
        "- Historical GREEN never certifies a newer failing critical workflow.",
        "- V0.2 does not delete, archive, or mutate product repositories automatically.",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({
        "scope_mode": scope_mode,
        "scan_complete": payload["scan_complete"],
        "counts": dict(counts),
        "missing_from_scan": missing_from_scan,
        "ungoverned": ungoverned,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
