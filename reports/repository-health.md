# JoyLab Repository Control Tower V0.2

- Generated: `2026-08-30T03:56:08.573859+00:00`
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

| Repository | State | Latest CI | Reason |
|---|---|---|---|
| ohbeopseok-ops/cs-ops-skills | **ACTIVE** | validate: success | pushed 0d ago |
| ohbeopseok-ops/joylab-agent-os | **ACTIVE** | JoyLab Release Gate: success | pushed 0d ago |
| ohbeopseok-ops/joylab-cs-adaptive-learning | **ACTIVE** | JoyLab Release Gate: success | pushed 0d ago |
| ohbeopseok-ops/joylab-etf-intelligence | **ACTIVE** | JoyLab Release Gate: success | pushed 0d ago |
| ohbeopseok-ops/joylab-money-os | **ACTIVE** | JoyLab Release Gate: success | pushed 0d ago |
| ohbeopseok-ops/joylab-search-engine | **ACTIVE** | JoyLab Release Gate: success | pushed 0d ago |
| ohbeopseok-ops/JoyLab-SEO | **ACTIVE** | JoyLab Release Gate: success | pushed 0d ago |
| ohbeopseok-ops/ohbeopseok-ops | **ACTIVE** | Repository Control Tower V0.1: success | pushed 0d ago |
| ohbeopseok-ops/https-github.com-uxjoseph-ppt_team_agent | **EMPTY** | none | repository size is 0 |
| ohbeopseok-ops/meeting | **EMPTY** | none | repository size is 0 |
| ohbeopseok-ops/codaro | **HEALTHY** | none | no current blocking signal |
| ohbeopseok-ops/dartlab | **HEALTHY** | none | no current blocking signal |
| ohbeopseok-ops/Hermes-Agent_One-Click_Kit | **HEALTHY** | none | no current blocking signal |
| ohbeopseok-ops/hyperframes | **HEALTHY** | none | no current blocking signal |
| ohbeopseok-ops/kordoc | **HEALTHY** | none | no current blocking signal |
| ohbeopseok-ops/- | **STALE** | none | no push for 248d |
| ohbeopseok-ops/copy-of-ai-meet | **STALE** | none | no push for 221d |
| ohbeopseok-ops/sales-point | **STALE** | none | no push for 254d |

## Automation contract

- **BROKEN** creates or refreshes one centralized managed issue per repository.
- Recovery automatically closes the managed issue.
- If a previously closed managed issue becomes BROKEN again, it reopens.
- Private coverage requires the `JOYLAB_GITHUB_TOKEN` repository secret.
