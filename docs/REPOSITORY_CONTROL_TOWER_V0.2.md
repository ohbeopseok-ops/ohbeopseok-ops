# JoyLab Repository Control Tower V0.2

## Goal

Scan all 44 owned repositories every day, including private repositories, and publish a deterministic health registry with portfolio ownership.

Outputs:

- `GITHUB_HEALTH_REGISTRY_V0.2.md`
- `control_tower/repository-health-v0.2.json`

Governance input:

- `control_tower/repository-governance.json`

## What changed from V0.1

1. Uses the six-state model: GREEN / YELLOW / RED / STALE / EMPTY / ARCHIVE.
2. Adds Core / Product / Experiment / Reference / Archive portfolio ownership.
3. Supports repository-specific critical and operational workflow names.
4. Distinguishes release blockers from operational automation failures.
5. Detects missing governed repositories and ungoverned new repositories.
6. Enforces the expected 44-repository full scan.
7. Refuses to silently certify a public-only scan as complete.

## Full private scan activation

GitHub's repository-scoped `GITHUB_TOKEN` cannot read every private repository owned by the account. Add the repository secret:

`CONTROL_TOWER_TOKEN`

with read access to all owned repositories and Actions metadata.

Until that secret exists, V0.2 will still generate a diagnostic snapshot but the **Validate generated JSON and governance coverage** step will fail rather than reporting a misleading GREEN full scan.

## Current remediation queue — 2026-09-23

| Priority | Repository | Finding | Root cause | Corrective action |
|---|---|---|---|---|
| P0 | joylab-content-os | Daily Scoring failed; GSC/NAVER scheduled jobs also failing | `SUPABASE_URL / SUPABASE_SECRET_KEY missing` in Actions runtime | restore/rotate required repository secrets and rerun scheduled pipelines |
| P1 | joylab-core8-engine | Portfolio Refresh and Dashboard Sync fail while Release Gate/CI/test are GREEN | `investment_lab_dashboard_sync.py` invoked without required `--sync` or `--check` | correct workflow/script invocation; keep engine health YELLOW, not RED |
| P1 | JoyLab-Book-Mining | Test Capture Engine and Release Gate fail | pytest cannot import `src`: `ModuleNotFoundError: No module named 'src'` | package/install project or set deterministic Python import path in CI |
| P2 | title-triumphs-tool | Release Gate stops at CI Install | `package-lock.json` is out of sync with `package.json`; `npm ci` reports many missing/invalid dependencies | regenerate lockfile with the intended Node/npm version, commit it, then restore strict `npm ci` |

## Interpretation rule

A scheduled operational failure does not automatically make the whole repository RED when critical release/test gates are GREEN. Repository-specific workflow policy in `repository-governance.json` decides whether the latest failure is RED or YELLOW.

## Daily schedule

The workflow runs at `22:17 UTC` (07:17 KST next day) and can also be run manually.
