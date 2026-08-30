#!/usr/bin/env python3
"""JoyLab Repository Control Tower V0.1.

Scans repositories owned by JOYLAB_GITHUB_OWNER and writes machine-readable
and Markdown health reports. Uses only the Python standard library.
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
TOKEN = os.getenv("JOYLAB_GITHUB_TOKEN") or os.getenv("GITHUB_TOKEN", "")
OUT_DIR = pathlib.Path(os.getenv("JOYLAB_CONTROL_TOWER_OUT", "reports"))
STALE_DAYS = int(os.getenv("JOYLAB_STALE_DAYS", "90"))
ACTIVE_DAYS = int(os.getenv("JOYLAB_ACTIVE_DAYS", "14"))

FAIL_CONCLUSIONS = {
    "failure", "cancelled", "timed_out", "action_required", "startup_failure",
}


def _request(path: str):
    url = path if path.startswith("https://") else f"https://api.github.com{path}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "joylab-repository-control-tower-v0.1",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def _paginate(path: str, per_page: int = 100):
    items = []
    page = 1
    while True:
        sep = "&" if "?" in path else "?"
        batch = _request(f"{path}{sep}per_page={per_page}&page={page}")
        if not isinstance(batch, list):
            raise RuntimeError(f"Expected list response for {path}")
        items.extend(batch)
        if len(batch) < per_page:
            return items
        page += 1


def discover_repositories():
    # /user/repos includes private repositories when JOYLAB_GITHUB_TOKEN is a
    # PAT/fine-grained token with repository read access. GITHUB_TOKEN fallback
    # generally sees only the controller repository and public resources.
    if TOKEN:
        repos = _paginate("/user/repos?affiliation=owner&sort=full_name")
        owned = [r for r in repos if r.get("owner", {}).get("login", "").lower() == OWNER.lower()]
        if owned:
            return owned, "authenticated-owner"
    return _paginate(f"/users/{urllib.parse.quote(OWNER)}/repos?type=owner&sort=full_name"), "public-only"


def latest_actions(repo_full_name: str):
    encoded = urllib.parse.quote(repo_full_name, safe="/")
    data = _request(f"/repos/{encoded}/actions/runs?per_page=20")
    runs = data.get("workflow_runs", [])
    if not runs:
        return None
    # Ignore this control-tower report itself when evaluating the controller repo
    # so the reporting workflow cannot mark itself healthy merely by running.
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
        counts[state] = counts.get(state, 0) + 1
        rows.append({
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
        })
    return {
        "schema_version": "0.1",
        "generated_at": now.isoformat(),
        "owner": OWNER,
        "scope": scope,
        "thresholds": {"active_days": ACTIVE_DAYS, "stale_days": STALE_DAYS},
        "counts": dict(sorted(counts.items())),
        "repositories": sorted(rows, key=lambda x: (x["state"], x["repository"].lower())),
    }


def render_markdown(report: dict):
    lines = [
        "# JoyLab Repository Control Tower V0.1",
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

    lines.extend([
        "",
        "## Repositories",
        "",
        "| Repository | State | Latest CI | Reason |",
        "|---|---|---|---|",
    ])
    for row in report["repositories"]:
        run = row.get("latest_workflow")
        ci = "none"
        if run:
            ci = f"{run.get('name')}: {run.get('conclusion') or run.get('status')}"
        reason = str(row.get("reason") or "").replace("|", "\\|")
        lines.append(f"| {row['repository']} | **{row['state']}** | {ci} | {reason} |")

    lines.extend([
        "",
        "## State contract",
        "",
        "- **BROKEN**: latest visible Actions run ended in failure/cancel/timeout/action-required.",
        "- **ACTIVE**: repository was pushed within the active window and has no visible blocker.",
        "- **HEALTHY**: no blocking signal and repository is between active/stale windows.",
        "- **STALE**: no push for the stale threshold.",
        "- **EMPTY**: repository size is zero.",
        "- **ARCHIVE**: GitHub repository is archived.",
        "",
        "> Private-repository coverage requires the `JOYLAB_GITHUB_TOKEN` Actions secret with read access to those repositories. Without it the report explicitly declares `public-only` scope.",
        "",
    ])
    return "\n".join(lines)


def main():
    now = dt.datetime.now(dt.timezone.utc)
    repos, scope = discover_repositories()
    report = build_report(repos, scope, now)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "repository-health.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (OUT_DIR / "repository-health.md").write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"scope": scope, "counts": report["counts"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
