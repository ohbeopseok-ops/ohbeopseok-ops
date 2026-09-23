# JoyLab Repository Control Tower V0.3

- Generated: `2026-09-23T12:59:53.834087+00:00`
- Owner: `ohbeopseok-ops`
- Discovery scope: **public-only**
- Thresholds: ACTIVE <= 14d, STALE >= 90d

## Summary

| State | Count |
|---|---:|
| BROKEN | 0 |
| ACTIVE | 6 |
| HEALTHY | 4 |
| STALE | 8 |
| EMPTY | 2 |
| ARCHIVE | 0 |

## Repositories

| Repository | Priority | Lifecycle | Readiness | State | Latest CI | Reason |
|---|---|---|---|---|---|---|
| ohbeopseok-ops/cs-ops-skills | **P1** | ACTIVE | 82 WATCH | **ACTIVE** | validate: success | pushed 9d ago |
| ohbeopseok-ops/joylab-etf-intelligence | **P1** | ACTIVE | 82 WATCH | **ACTIVE** | Gate Scan Alerts: success | pushed 0d ago |
| ohbeopseok-ops/joylab-publishing-os | **P1** | ACTIVE | 82 WATCH | **ACTIVE** | Build: success | pushed 0d ago |
| ohbeopseok-ops/JoyLab-SEO | **P1** | ACTIVE | 92 READY | **ACTIVE** | JoyLab Release Gate: success | pushed 2d ago |
| ohbeopseok-ops/ohbeopseok-ops | **P1** | ACTIVE | 62 BLOCKED | **ACTIVE** | Repository Control Tower V0.2: in_progress | pushed 0d ago |
| ohbeopseok-ops/senior-toilet-finder | **P1** | ACTIVE | 82 WATCH | **ACTIVE** | Geocode Public Toilet Addresses: success | pushed 0d ago |
| ohbeopseok-ops/https-github.com-uxjoseph-ppt_team_agent | **P2** | ARCHIVE | 40 BLOCKED | **EMPTY** | none | repository size is 0 |
| ohbeopseok-ops/meeting | **P2** | ARCHIVE | 40 BLOCKED | **EMPTY** | none | repository size is 0 |
| ohbeopseok-ops/joylab-agent-os | **P0** | ACTIVE | 87 WATCH | **HEALTHY** | JoyLab Release Gate: success | no current blocking signal |
| ohbeopseok-ops/joylab-cs-adaptive-learning | **P2** | MAINTENANCE | 87 WATCH | **HEALTHY** | JoyLab Release Gate: success | no current blocking signal |
| ohbeopseok-ops/joylab-money-os | **P1** | ACTIVE | 87 WATCH | **HEALTHY** | JoyLab Release Gate: success | no current blocking signal |
| ohbeopseok-ops/joylab-search-engine | **P2** | MAINTENANCE | 87 WATCH | **HEALTHY** | JoyLab Release Gate: success | no current blocking signal |
| ohbeopseok-ops/- | **P2** | MAINTENANCE | 47 BLOCKED | **STALE** | none | no push for 273d |
| ohbeopseok-ops/codaro | **P2** | MAINTENANCE | 47 BLOCKED | **STALE** | none | no push for 105d |
| ohbeopseok-ops/copy-of-ai-meet | **P2** | MAINTENANCE | 47 BLOCKED | **STALE** | none | no push for 245d |
| ohbeopseok-ops/dartlab | **P2** | MAINTENANCE | 47 BLOCKED | **STALE** | none | no push for 104d |
| ohbeopseok-ops/Hermes-Agent_One-Click_Kit | **P2** | MAINTENANCE | 47 BLOCKED | **STALE** | none | no push for 103d |
| ohbeopseok-ops/hyperframes | **P2** | MAINTENANCE | 47 BLOCKED | **STALE** | none | no push for 104d |
| ohbeopseok-ops/kordoc | **P2** | MAINTENANCE | 47 BLOCKED | **STALE** | none | no push for 104d |
| ohbeopseok-ops/sales-point | **P2** | MAINTENANCE | 47 BLOCKED | **STALE** | none | no push for 279d |

## Automation contract

- **BROKEN** creates or refreshes one centralized managed issue per repository.
- Recovery automatically closes the managed issue.
- If a previously closed managed issue becomes BROKEN again, it reopens.
- Private coverage requires the `JOYLAB_GITHUB_TOKEN` repository secret.
