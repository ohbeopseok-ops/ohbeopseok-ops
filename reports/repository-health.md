# JoyLab Repository Control Tower V0.3

- Generated: `2026-08-31T00:35:34.386747+00:00`
- Owner: `ohbeopseok-ops`
- Discovery scope: **public-only**
- Thresholds: ACTIVE <= 14d, STALE >= 90d

## Summary

| State | Count |
|---|---:|
| BROKEN | 0 |
| ACTIVE | 8 |
| HEALTHY | 5 |
| STALE | 3 |
| EMPTY | 2 |
| ARCHIVE | 0 |

## Repositories

| Repository | Priority | Lifecycle | Readiness | State | Latest CI | Reason |
|---|---|---|---|---|---|---|
| ohbeopseok-ops/cs-ops-skills | **P1** | ACTIVE | 82 WATCH | **ACTIVE** | validate: success | pushed 0d ago |
| ohbeopseok-ops/joylab-agent-os | **P0** | ACTIVE | 92 READY | **ACTIVE** | JoyLab Release Gate: success | pushed 0d ago |
| ohbeopseok-ops/joylab-cs-adaptive-learning | **P1** | ACTIVE | 92 READY | **ACTIVE** | JoyLab Release Gate: success | pushed 0d ago |
| ohbeopseok-ops/joylab-etf-intelligence | **P1** | ACTIVE | 92 READY | **ACTIVE** | JoyLab Release Gate: success | pushed 0d ago |
| ohbeopseok-ops/joylab-money-os | **P1** | ACTIVE | 92 READY | **ACTIVE** | JoyLab Release Gate: success | pushed 0d ago |
| ohbeopseok-ops/joylab-search-engine | **P1** | ACTIVE | 92 READY | **ACTIVE** | JoyLab Release Gate: success | pushed 0d ago |
| ohbeopseok-ops/JoyLab-SEO | **P1** | ACTIVE | 92 READY | **ACTIVE** | JoyLab Release Gate: success | pushed 0d ago |
| ohbeopseok-ops/ohbeopseok-ops | **P1** | ACTIVE | 82 WATCH | **ACTIVE** | Control Tower CI: success | pushed 0d ago |
| ohbeopseok-ops/https-github.com-uxjoseph-ppt_team_agent | **P2** | ARCHIVE | 40 BLOCKED | **EMPTY** | none | repository size is 0 |
| ohbeopseok-ops/meeting | **P2** | ARCHIVE | 40 BLOCKED | **EMPTY** | none | repository size is 0 |
| ohbeopseok-ops/codaro | **P2** | MAINTENANCE | 52 BLOCKED | **HEALTHY** | none | no current blocking signal |
| ohbeopseok-ops/dartlab | **P2** | MAINTENANCE | 52 BLOCKED | **HEALTHY** | none | no current blocking signal |
| ohbeopseok-ops/Hermes-Agent_One-Click_Kit | **P2** | MAINTENANCE | 52 BLOCKED | **HEALTHY** | none | no current blocking signal |
| ohbeopseok-ops/hyperframes | **P2** | MAINTENANCE | 52 BLOCKED | **HEALTHY** | none | no current blocking signal |
| ohbeopseok-ops/kordoc | **P2** | MAINTENANCE | 52 BLOCKED | **HEALTHY** | none | no current blocking signal |
| ohbeopseok-ops/- | **P2** | MAINTENANCE | 47 BLOCKED | **STALE** | none | no push for 249d |
| ohbeopseok-ops/copy-of-ai-meet | **P2** | MAINTENANCE | 47 BLOCKED | **STALE** | none | no push for 221d |
| ohbeopseok-ops/sales-point | **P2** | MAINTENANCE | 47 BLOCKED | **STALE** | none | no push for 255d |

## Automation contract

- **BROKEN** creates or refreshes one centralized managed issue per repository.
- Recovery automatically closes the managed issue.
- If a previously closed managed issue becomes BROKEN again, it reopens.
- Private coverage requires the `JOYLAB_GITHUB_TOKEN` repository secret.
