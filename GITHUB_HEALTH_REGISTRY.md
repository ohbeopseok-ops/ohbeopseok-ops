# JoyLab GitHub Health Registry

Snapshot: 2026-08-30 KST

## Classification rules

- **ACTIVE** — active development or an open PR is currently moving.
- **BROKEN** — a known CI failure, merge conflict, missing release validation, or other blocker prevents promotion.
- **HEALTHY** — recent repository activity with no known blocking failure.
- **STALE** — non-empty repository with no meaningful recent maintenance or with aging unfinished work.
- **EMPTY** — repository has no committed project payload.
- **ARCHIVE** — abandoned/one-off/placeholder repository that should normally be archived after owner review.

> This registry is an operational snapshot, not a permanent label. A repository can move between states after CI, merge, or release evidence changes.

| Repository | State | Evidence / next action |
|---|---|---|
| meeting | EMPTY | size 0; decide initialize vs archive |
| sales-point | ARCHIVE | only initial Vercel commit from 2025-12; archive candidate |
| - | ARCHIVE | placeholder-style name and minimal payload; archive candidate |
| https-github.com-uxjoseph-ppt_team_agent | EMPTY | size 0; archive candidate |
| risk-zero | ARCHIVE | only initial Vercel commit from 2026-01; archive candidate |
| basic-comics | EMPTY | size 0 |
| copy-of-ai-meet | ARCHIVE | one initial Vercel commit from 2026-01; archive candidate |
| cs-ops-skills | STALE | main activity old and PRs accumulated; review/close or refresh PRs |
| JoyLab-SEO | ACTIVE | recent baseline work; needs executable CI/release contract |
| title-triumphs-tool | ACTIVE | repaired CI; latest router validation Install → Gold Case → Build is GREEN |
| dartlab | STALE | last main activity 2026-06; review maintenance ownership |
| codaro | STALE | last main activity 2026-06; review release/CI state |
| hyperframes | STALE | last release activity 2026-06; review maintenance ownership |
| kordoc | STALE | publish workflow was intentionally removed; release process needs explicit gate |
| Hermes-Agent_One-Click_Kit | STALE | last main activity 2026-06; refresh or archive |
| joylab-html-tool | BROKEN | stale PR replaced, but current validation branch has no Actions run; CI trigger/coverage missing |
| joylab-vercel-site | HEALTHY | recent repository split cleanup; no known blocker |
| onboaring | EMPTY | size 0 |
| on_0720 | EMPTY | size 0 |
| masterplan_0722 | EMPTY | size 0 |
| desktop-tutorial | EMPTY | size 0 |
| joylab_ai_coach_tutor | EMPTY | size 0 |
| JoyLab_Vibe_Coding_OS_v1.0 | HEALTHY | active documentation/engineering-standard work |
| joylab-knowledge-os | ACTIVE | P1 Gold Case runner repaired; latest D2S CI GREEN |
| joylab-cs-adaptive-learning | HEALTHY | recent structured-output compatibility fix |
| joylab-ai-voice-benchmark | ACTIVE | current evidence-foundation/backend CI GREEN |
| JoyLab-Book-Mining | HEALTHY | Capture Engine V0.2 + regression workflow recently added |
| joylab-core8-engine | BROKEN | #13 merged, but #12/#10 require rebase and #8 has failing CI |
| ohbeopseok-ops | HEALTHY | profile/operational repository; recent maintenance |
| joylab-product-hub | HEALTHY | recent split/upload activity; no known blocker |
| joylab-etf-intelligence | HEALTHY | JoyLab CI Standard V1.0 adopted |
| joylab-search-engine | ACTIVE | Trust Layer PR CI GREEN |
| joylab-cs-accuracy-os | HEALTHY | 84/84 tests + reproducible Windows build evidence recorded |
| joylab-agent-os | ACTIVE | Vercel adapter import fix applied; Python 3.11/3.12/3.13 + certification gate GREEN |
| joylab-money-os | ACTIVE | portable EXE build path under active validation |

## Current P0 / P1 queue

1. **P0 — joylab-core8-engine #8**: fix failing test + ci-standard-v1.
2. **P0 — joylab-html-tool**: restore a real PR-triggered Windows/Tauri Actions workflow.
3. **P1 — joylab-core8-engine #12**: resolve conflict after retarget to main, then rerun test + ci-standard-v1.
4. **P1 — joylab-core8-engine #10**: rebase onto current main, then rerun GREEN gates.
5. **P1 — core8 #1/#3/#6**: preserve unique assets, but rebase/scope-reduce before any merge.
6. **P2 — EMPTY/ARCHIVE group**: archive after owner review; do not spend CI effort on empty placeholders.

## Promotion rule

A repository is release-ready only when:

`CI → Gold Case → Regression → Build → Release Gate`

all required stages are GREEN for the current main-compatible commit. A stale GREEN result is not sufficient.
