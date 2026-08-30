# JoyLab Repository Control Tower V0.3

- Generated: `2026-08-30T04:22:14.441472+00:00`
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

| Repository | Priority | Lifecycle | State | Latest CI | Reason |
|---|---|---|---|---|---|
| ohbeopseok-ops/cs-ops-skills | **P1** | ACTIVE | **ACTIVE** | validate: success | pushed 0d ago |
| ohbeopseok-ops/joylab-agent-os | **P0** | ACTIVE | **ACTIVE** | JoyLab Release Gate: success | pushed 0d ago |
| ohbeopseok-ops/joylab-cs-adaptive-learning | **P1** | ACTIVE | **ACTIVE** | JoyLab Release Gate: success | pushed 0d ago |
| ohbeopseok-ops/joylab-etf-intelligence | **P1** | ACTIVE | **ACTIVE** | JoyLab Release Gate: success | pushed 0d ago |
| ohbeopseok-ops/joylab-money-os | **P1** | ACTIVE | **ACTIVE** | JoyLab Release Gate: success | pushed 0d ago |
| ohbeopseok-ops/joylab-search-engine | **P1** | ACTIVE | **ACTIVE** | JoyLab Release Gate: success | pushed 0d ago |
| ohbeopseok-ops/JoyLab-SEO | **P1** | ACTIVE | **ACTIVE** | JoyLab Release Gate: success | pushed 0d ago |
| ohbeopseok-ops/ohbeopseok-ops | **P1** | ACTIVE | **ACTIVE** | Repository Control Tower V0.1: success | pushed 0d ago |
| ohbeopseok-ops/https-github.com-uxjoseph-ppt_team_agent | **P2** | ARCHIVE | **EMPTY** | none | repository size is 0 |
| ohbeopseok-ops/meeting | **P2** | ARCHIVE | **EMPTY** | none | repository size is 0 |
| ohbeopseok-ops/codaro | **P2** | MAINTENANCE | **HEALTHY** | none | no current blocking signal |
| ohbeopseok-ops/dartlab | **P2** | MAINTENANCE | **HEALTHY** | none | no current blocking signal |
| ohbeopseok-ops/Hermes-Agent_One-Click_Kit | **P2** | MAINTENANCE | **HEALTHY** | none | no current blocking signal |
| ohbeopseok-ops/hyperframes | **P2** | MAINTENANCE | **HEALTHY** | none | no current blocking signal |
| ohbeopseok-ops/kordoc | **P2** | MAINTENANCE | **HEALTHY** | none | no current blocking signal |
| ohbeopseok-ops/- | **P2** | MAINTENANCE | **STALE** | none | no push for 248d |
| ohbeopseok-ops/copy-of-ai-meet | **P2** | MAINTENANCE | **STALE** | none | no push for 221d |
| ohbeopseok-ops/sales-point | **P2** | MAINTENANCE | **STALE** | none | no push for 254d |

## Automation contract

- **BROKEN** creates or refreshes one centralized managed issue per repository.
- Recovery automatically closes the managed issue.
- If a previously closed managed issue becomes BROKEN again, it reopens.
- Private coverage requires the `JOYLAB_GITHUB_TOKEN` repository secret.
