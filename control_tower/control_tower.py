#!/usr/bin/env python3
"""JoyLab Repository Control Tower V0.3.

Scans JoyLab repositories, writes health reports, and reconciles centralized
BROKEN issues. Standard-library only.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import pathlib
import urllib.error
import urllib.parse
import urllib.request

OWNER = os.getenv("JOYLAB_GITHUB_OWNER", "ohbeopseok-ops")
PRIVATE_TOKEN = os.getenv("JOYLAB_GITHUB_TOKEN", "")
WRITE_TOKEN = os.getenv("GITHUB_TOKEN", "")
READ_TOKEN = PRIVATE_TOKEN or WRITE_TOKEN
CONTROLLER_REPO = os.getenv("JOYLAB_CONTROLLER_REPO") or os.getenv("GITHUB_REPOSITORY", f"{OWNER}/{OWNER}")
OUT_DIR = pathlib.Path(os.getenv("JOYLAB_CONTROL_TOWER_OUT", "reports"))
STALE_DAYS = int(os.getenv("JOYLAB_STALE_DAYS", "90"))
ACTIVE_DAYS = int(os.getenv("JOYLAB_ACTIVE_DAYS", "14"))

FAIL_CONCLUSIONS = {
    "failure", "cancelled", "timed_out", "action_required", "startup_failure",
}
ISSUE_MARKER_PREFIX = "<!-- joylab-control-tower:repo="
ISSUE_TITLE_PREFIX = "[BROKEN] "


def _request(path: str, *, token: str | None = None, method: str = "GET", data: dict | None = None):
    url = path if path.startswith("https://") else f"https://api.github.com{path}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "joylab-repository-control-tower-v0.3",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    payload = None
    if data is not None:
        headers["Content-Type"] = "application/json"
        payload = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, headers=headers, data=payload, method=method)
    with urllib.request.urlopen(req, timeout=30) as response:
        raw = response.read().decode("utf-8")
        return json.loads(raw) if raw else {}


def _paginate(path: str, *, token: str | None = None, per_page: int = 100):
    items = []
    page = 1
    while True:
        sep = "&" if "?" in path else "?"
        batch = _request(f"{path}{sep}per_page={per_page}&page={page}", token=token)
        if not isinstance(batch, list):
            raise RuntimeError(f"Expected list response for {path}")
        items.extend(batch)
        if len(batch) < per_page:
            return items
        page += 1


def discover_repositories():
    if PRIVATE_TOKEN:
        repos = _paginate("/user/repos?affiliation=owner&sort=full_name", token=PRIVATE_TOKEN)
        owned = [r for r in repos if r.get("owner", {}).get("login", "").lower() == OWNER.lower()]
        if owned:
            return owned, "authenticated-owner"
    return (
        _paginate(
            f"/users/{urllib.parse.quote(OWNER)}/repos?type=owner&sort=full_name",
            token=WRITE_TOKEN or None,
        ),
        "public-only",
    )


def latest_actions(repo_full_name: str):
    encoded = urllib.parse.quote(repo_full_name, safe="/")
    data = _request(f"/repos/{encoded}/actions/runs?per_page=20", token=READ_TOKEN or None)
    runs = data.get("workflow_runs", [])
    if not runs:
        return None
    for run in runs:
        if run.get("name") != "JoyLab Repository Control Tower":
            return {
                "id": run.get("id"),
                "name": run.get("name"),
                "status": run.get("status"),
                "conclusion": run.get("conclusion"),
                "event": run.get("event"),
                "head_sha": run.get("head_sha"),
                "html_url": run.get("html_url"),
                "updated_at": run.get("updated_at"),
            }
    return None



def _job_logs(repo_full_name: str, job_id: int) -> str:
    encoded = urllib.parse.quote(repo_full_name, safe="/")
    url = f"https://api.github.com/repos/{encoded}/actions/jobs/{job_id}/logs"
    headers = {"User-Agent": "joylab-repository-control-tower-v0.3"}
    if READ_TOKEN:
        headers["Authorization"] = f"Bearer {READ_TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def diagnose_failure(repo_full_name: str, run: dict | None) -> dict | None:
    if not run or run.get("conclusion") not in FAIL_CONCLUSIONS or not run.get("id"):
        return None
    encoded = urllib.parse.quote(repo_full_name, safe="/")
    data = _request(f"/repos/{encoded}/actions/runs/{run['id']}/jobs?per_page=100", token=READ_TOKEN or None)
    failed = [j for j in data.get("jobs", []) if j.get("conclusion") == "failure"]
    if not failed:
        return {"failed_job": None, "failed_step": None, "root_cause": "Workflow failed but no failed job was visible.", "fix_candidate": "Inspect workflow-level configuration and permissions."}
    job = failed[0]
    steps = [s for s in job.get("steps", []) if s.get("conclusion") == "failure"]
    step = steps[0].get("name") if steps else None
    try:
        log = _job_logs(repo_full_name, int(job["id"]))
    except Exception as exc:
        log = f"log unavailable: {exc}"
    tail = "\n".join(log.splitlines()[-180:])
    patterns = [
        ("ModuleNotFoundError", "Python import path/package mismatch", "Align imports and PYTHONPATH/package layout; rerun collection and unit tests."),
        ("npm ci can only install", "package-lock.json is out of sync with package.json", "Regenerate and commit the lockfile, then restore strict npm ci."),
        ("ERESOLVE", "npm dependency resolution conflict", "Reconcile dependency versions and regenerate the lockfile."),
        ("SyntaxError", "syntax error introduced by the current change", "Fix the reported syntax location and add a regression test."),
        ("AssertionError", "test expectation or runtime behavior mismatch", "Inspect the first failing assertion and apply the smallest behavior/fixture correction."),
        ("HTTP Error 403", "GitHub/API permission denied", "Adjust least-privilege token/workflow permissions for the failed API call."),
        ("non-fast-forward", "concurrent or stale git push", "Fetch/rebase before push or serialize publishing."),
        ("No module named", "Python module import failure", "Align import path with the installed package and pytest pythonpath."),
    ]
    root = "Unclassified failure; inspect the extracted error tail."
    fix = "Use the failed job/step and log tail to create a minimal recovery change."
    for needle, cause, candidate in patterns:
        if needle in tail:
            root, fix = cause, candidate
            break
    error_lines = [ln.strip() for ln in tail.splitlines() if any(k in ln for k in ("ERROR", "Error:", "E   ", "##[error]", "FAILED"))]
    return {
        "failed_job": job.get("name"),
        "failed_step": step,
        "root_cause": root,
        "fix_candidate": fix,
        "error_excerpt": error_lines[-3:],
    }

def classify(repo: dict, latest_run: dict | None, now: dt.datetime):
    if repo.get("archived"):
        return "ARCHIVE", "repository archived"
    if int(repo.get("size") or 0) == 0:
        return "EMPTY", "repository size is 0"
    if latest_run and latest_run.get("conclusion") in FAIL_CONCLUSIONS:
        return "BROKEN", f"latest workflow {latest_run.get('name')}={latest_run.get('conclusion')}"

    pushed = repo.get("pushed_at")
    age_days = None
    if pushed:
        pushed_at = dt.datetime.fromisoformat(pushed.replace("Z", "+00:00"))
        age_days = max(0, (now - pushed_at).days)

    if age_days is not None and age_days <= ACTIVE_DAYS:
        return "ACTIVE", f"pushed {age_days}d ago"
    if age_days is not None and age_days >= STALE_DAYS:
        return "STALE", f"no push for {age_days}d"
    return "HEALTHY", "no current blocking signal"



def portfolio_governance(row: dict) -> dict:
    state = row["state"]
    if state == "BROKEN":
        priority, lifecycle = "P0", "ACTIVE"
    elif state == "ACTIVE":
        priority, lifecycle = "P1", "ACTIVE"
    elif state in {"HEALTHY", "STALE"}:
        priority, lifecycle = "P2", "MAINTENANCE"
    else:
        priority, lifecycle = "P2", "ARCHIVE"

    overrides = {
        "ohbeopseok-ops/joylab-core8-engine": ("P0", "ACTIVE"),
        "ohbeopseok-ops/joylab-agent-os": ("P0", "ACTIVE"),
        "ohbeopseok-ops/joylab-ai-voice-benchmark": ("P1", "ACTIVE"),
        "ohbeopseok-ops/joylab-money-os": ("P1", "ACTIVE"),
        "ohbeopseok-ops/joylab-html-tool": ("P1", "ACTIVE"),
    }
    if row["repository"] in overrides:
        priority, lifecycle = overrides[row["repository"]]
    return {"priority": priority, "lifecycle": lifecycle}

def build_report(repos: list[dict], scope: str, now: dt.datetime):
    rows = []
    counts = {}
    for repo in repos:
        full_name = repo["full_name"]
        try:
            run = latest_actions(full_name)
            actions_error = None
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
            run = None
            actions_error = str(exc)

        state, reason = classify(repo, run, now)
        diagnosis = diagnose_failure(full_name, run) if state == "BROKEN" else None
        counts[state] = counts.get(state, 0) + 1
        row = {
            "repository": full_name,
            "visibility": repo.get("visibility") or ("private" if repo.get("private") else "public"),
            "default_branch": repo.get("default_branch"),
            "archived": bool(repo.get("archived")),
            "size": repo.get("size"),
            "pushed_at": repo.get("pushed_at"),
            "state": state,
            "reason": reason,
            "latest_workflow": run,
            "actions_error": actions_error,
            "diagnosis": diagnosis,
        }
        row["governance"] = portfolio_governance(row)
        rows.append(row)
    return {
        "schema_version": "0.3",
        "generated_at": now.isoformat(),
        "owner": OWNER,
        "scope": scope,
        "thresholds": {"active_days": ACTIVE_DAYS, "stale_days": STALE_DAYS},
        "counts": dict(sorted(counts.items())),
        "repositories": sorted(rows, key=lambda x: (x["state"], x["repository"].lower())),
    }


def issue_marker(repo_full_name: str) -> str:
    return f"{ISSUE_MARKER_PREFIX}{repo_full_name} -->"


def managed_repo_from_issue(issue: dict) -> str | None:
    body = issue.get("body") or ""
    start = body.find(ISSUE_MARKER_PREFIX)
    if start < 0:
        return None
    start += len(ISSUE_MARKER_PREFIX)
    end = body.find(" -->", start)
    return body[start:end] if end > start else None


def issue_body(row: dict) -> str:
    run = row.get("latest_workflow") or {}
    run_url = run.get("html_url") or "n/a"
    return "\n".join([
        issue_marker(row["repository"]),
        "## JoyLab Repository Control Tower V0.3",
        "",
        f"**Repository:** `{row['repository']}`",
        f"**State:** **BROKEN**",
        f"**Reason:** {row.get('reason')}",
        f"**Latest workflow:** {run.get('name') or 'unknown'}",
        f"**Workflow result:** {run.get('conclusion') or run.get('status') or 'unknown'}",
        f"**Workflow:** {run_url}",
        f"**Failed job:** {(row.get('diagnosis') or {}).get('failed_job') or 'unknown'}",
        f"**Failed step:** {(row.get('diagnosis') or {}).get('failed_step') or 'unknown'}",
        f"**Root cause:** {(row.get('diagnosis') or {}).get('root_cause') or 'unclassified'}",
        f"**FIX CANDIDATE:** {(row.get('diagnosis') or {}).get('fix_candidate') or 'inspect failure log'}",
        "",
        "### Recovery gate",
        "1. Identify failed job/step and root cause.",
        "2. Apply the smallest reproducible fix.",
        "3. Re-run CI / Gold Case / Regression / Build as applicable.",
        "4. This issue closes automatically after the repository is no longer BROKEN.",
        "",
        f"_Last observed: {row.get('pushed_at') or 'unknown'}_",
    ])


def plan_issue_actions(report: dict, issues: list[dict]):
    managed = {}
    for issue in issues:
        repo = managed_repo_from_issue(issue)
        if repo:
            managed[repo] = issue

    broken = {r["repository"]: r for r in report["repositories"] if r["state"] == "BROKEN"}
    actions = []

    for repo_name, row in broken.items():
        issue = managed.get(repo_name)
        if issue is None:
            actions.append(("create", repo_name, row, None))
        elif issue.get("state") == "closed":
            actions.append(("reopen", repo_name, row, issue))
        else:
            actions.append(("refresh", repo_name, row, issue))

    for repo_name, issue in managed.items():
        if repo_name not in broken and issue.get("state") == "open":
            actions.append(("close", repo_name, None, issue))
    return actions


def reconcile_broken_issues(report: dict):
    if not WRITE_TOKEN:
        return {"mode": "disabled", "reason": "GITHUB_TOKEN unavailable", "actions": []}

    encoded = urllib.parse.quote(CONTROLLER_REPO, safe="/")
    issues = _paginate(f"/repos/{encoded}/issues?state=all", token=WRITE_TOKEN)
    issues = [i for i in issues if "pull_request" not in i]
    planned = plan_issue_actions(report, issues)
    applied = []

    for action, repo_name, row, issue in planned:
        if action == "create":
            payload = {
                "title": ISSUE_TITLE_PREFIX + repo_name,
                "body": issue_body(row),
                "labels": ["control-tower", "broken-ci"],
            }
            try:
                created = _request(f"/repos/{encoded}/issues", token=WRITE_TOKEN, method="POST", data=payload)
            except urllib.error.HTTPError as exc:
                if exc.code == 422:
                    payload.pop("labels", None)
                    created = _request(f"/repos/{encoded}/issues", token=WRITE_TOKEN, method="POST", data=payload)
                else:
                    raise
            applied.append({"action": action, "repository": repo_name, "issue": created.get("number")})
        elif action in {"reopen", "refresh"}:
            payload = {"body": issue_body(row)}
            if action == "reopen":
                payload["state"] = "open"
            updated = _request(
                f"/repos/{encoded}/issues/{issue['number']}",
                token=WRITE_TOKEN,
                method="PATCH",
                data=payload,
            )
            applied.append({"action": action, "repository": repo_name, "issue": updated.get("number")})
        elif action == "close":
            updated = _request(
                f"/repos/{encoded}/issues/{issue['number']}",
                token=WRITE_TOKEN,
                method="PATCH",
                data={"state": "closed", "state_reason": "completed"},
            )
            applied.append({"action": action, "repository": repo_name, "issue": updated.get("number")})
    return {"mode": "enabled", "actions": applied}


def render_markdown(report: dict):
    lines = [
        "# JoyLab Repository Control Tower V0.3",
        "",
        f"- Generated: `{report['generated_at']}`",
        f"- Owner: `{report['owner']}`",
        f"- Discovery scope: **{report['scope']}**",
        f"- Thresholds: ACTIVE <= {report['thresholds']['active_days']}d, STALE >= {report['thresholds']['stale_days']}d",
        "",
        "## Summary",
        "",
        "| State | Count |",
        "|---|---:|",
    ]
    for state in ["BROKEN", "ACTIVE", "HEALTHY", "STALE", "EMPTY", "ARCHIVE"]:
        lines.append(f"| {state} | {report['counts'].get(state, 0)} |")

    lines.extend(["", "## Repositories", "", "| Repository | Priority | Lifecycle | State | Latest CI | Reason |", "|---|---|---|---|---|---|"])
    for row in report["repositories"]:
        run = row.get("latest_workflow")
        ci = "none"
        if run:
            ci = f"{run.get('name')}: {run.get('conclusion') or run.get('status')}"
        reason = str(row.get("reason") or "").replace("|", "\\|")
        gov = row.get("governance") or {}
        lines.append(f"| {row['repository']} | **{gov.get('priority', 'P2')}** | {gov.get('lifecycle', 'MAINTENANCE')} | **{row['state']}** | {ci} | {reason} |")

    lines.extend([
        "",
        "## Automation contract",
        "",
        "- **BROKEN** creates or refreshes one centralized managed issue per repository.",
        "- Recovery automatically closes the managed issue.",
        "- If a previously closed managed issue becomes BROKEN again, it reopens.",
        "- Private coverage requires the `JOYLAB_GITHUB_TOKEN` repository secret.",
        "",
    ])
    return "\n".join(lines)


def main():
    now = dt.datetime.now(dt.timezone.utc)
    repos, scope = discover_repositories()
    report = build_report(repos, scope, now)
    issue_result = reconcile_broken_issues(report)
    report["issue_reconciliation"] = issue_result

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "repository-health.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (OUT_DIR / "repository-health.md").write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({
        "scope": scope,
        "counts": report["counts"],
        "issue_actions": issue_result.get("actions", []),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
