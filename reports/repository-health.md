# JoyLab Repository Control Tower V0.3

- Generated: `2026-09-21T00:13:55.508296+00:00`
- Owner: `ohbeopseok-ops`
- Discovery scope: **public-only**
- Thresholds: ACTIVE <= 14d, STALE >= 90d

## Summary

| State | Count |
|---|---:|
| BROKEN | 1 |
| ACTIVE | 5 |
| HEALTHY | 3 |
| STALE | 8 |
| EMPTY | 2 |
| ARCHIVE | 0 |

## Repositories

| Repository | Priority | Lifecycle | Readiness | State | Latest CI | Reason |
|---|---|---|---|---|---|---|
| ohbeopseok-ops/cs-ops-skills | **P1** | ACTIVE | 82 WATCH | **ACTIVE** | validate: success | pushed 7d ago |
| ohbeopseok-ops/joylab-agent-os | **P0** | ACTIVE | 92 READY | **ACTIVE** | JoyLab Release Gate: success | pushed 14d ago |
| ohbeopseok-ops/joylab-etf-intelligence | **P1** | ACTIVE | 82 WATCH | **ACTIVE** | Gate Scan Alerts: success | pushed 2d ago |
| ohbeopseok-ops/joylab-publishing-os | **P1** | ACTIVE | 82 WATCH | **ACTIVE** | Research Evidence Audit: success | pushed 0d ago |
| ohbeopseok-ops/JoyLab-SEO | **P1** | ACTIVE | 92 READY | **ACTIVE** | JoyLab Release Gate: success | pushed 0d ago |
| ohbeopseok-ops/ohbeopseok-ops | **P0** | ACTIVE | 27 BLOCKED | **BROKEN** | Repository Control Tower V0.1: failure | latest workflow Repository Control Tower V0.1=failure |
| ohbeopseok-ops/https-github.com-uxjoseph-ppt_team_agent | **P2** | ARCHIVE | 40 BLOCKED | **EMPTY** | none | repository size is 0 |
| ohbeopseok-ops/meeting | **P2** | ARCHIVE | 40 BLOCKED | **EMPTY** | none | repository size is 0 |
| ohbeopseok-ops/joylab-cs-adaptive-learning | **P2** | MAINTENANCE | 87 WATCH | **HEALTHY** | JoyLab Release Gate: success | no current blocking signal |
| ohbeopseok-ops/joylab-money-os | **P1** | ACTIVE | 87 WATCH | **HEALTHY** | JoyLab Release Gate: success | no current blocking signal |
| ohbeopseok-ops/joylab-search-engine | **P2** | MAINTENANCE | 87 WATCH | **HEALTHY** | JoyLab Release Gate: success | no current blocking signal |
| ohbeopseok-ops/- | **P2** | MAINTENANCE | 47 BLOCKED | **STALE** | none | no push for 270d |
| ohbeopseok-ops/codaro | **P2** | MAINTENANCE | 47 BLOCKED | **STALE** | none | no push for 102d |
| ohbeopseok-ops/copy-of-ai-meet | **P2** | MAINTENANCE | 47 BLOCKED | **STALE** | none | no push for 242d |
| ohbeopseok-ops/dartlab | **P2** | MAINTENANCE | 47 BLOCKED | **STALE** | none | no push for 101d |
| ohbeopseok-ops/Hermes-Agent_One-Click_Kit | **P2** | MAINTENANCE | 47 BLOCKED | **STALE** | none | no push for 101d |
| ohbeopseok-ops/hyperframes | **P2** | MAINTENANCE | 47 BLOCKED | **STALE** | none | no push for 101d |
| ohbeopseok-ops/kordoc | **P2** | MAINTENANCE | 47 BLOCKED | **STALE** | none | no push for 101d |
| ohbeopseok-ops/sales-point | **P2** | MAINTENANCE | 47 BLOCKED | **STALE** | none | no push for 276d |

## Automation contract

- **BROKEN** creates or refreshes one centralized managed issue per repository.
- Recovery automatically closes the managed issue.
- If a previously closed managed issue becomes BROKEN again, it reopens.
- Private coverage requires the `JOYLAB_GITHUB_TOKEN` repository secret.
