# JoyLab GitHub Health Registry

Snapshot: 2026-08-30 KST — Recovery Pass 2

## Classification rules

- **ACTIVE** — active development or a governed follow-up remains.
- **BROKEN** — a known CI/release blocker prevents promotion.
- **HEALTHY** — recent repository activity with no known blocking failure.
- **STALE** — non-empty repository with no meaningful recent maintenance or aging unfinished work.
- **EMPTY** — repository has no committed project payload.
- **ARCHIVE** — abandoned/one-off/placeholder repository that should normally be archived after owner review.

> This is a manually curated full-account snapshot. The automated Control Tower V0.1 currently falls back to public repositories unless CONTROL_TOWER_TOKEN is configured for cross-repository private access.

| Repository | State | Evidence / next action |
|---|---|---|
| meeting | EMPTY | size 0; decide initialize vs archive |
| sales-point | ARCHIVE | only initial Vercel commit from 2025-12; archive candidate |
| - | ARCHIVE | placeholder-style name and minimal payload; archive candidate |
| https-github.com-uxjoseph-ppt_team_agent | EMPTY | size 0; archive candidate |
| risk-zero | ARCHIVE | only initial Vercel commit from 2026-01; archive candidate |
| basic-comics | EMPTY | size 0 |
| copy-of-ai-meet | ARCHIVE | one initial Vercel commit from 2026-01; archive candidate |
| cs-ops-skills | STALE | aging PRs; review/close or refresh |
| JoyLab-SEO | ACTIVE | JoyLab Release Gate caller adopted |
| title-triumphs-tool | ACTIVE | CI repaired; Install → Gold Case → Build GREEN; synchronize package-lock then restore strict npm ci |
| dartlab | STALE | last main activity 2026-06; review maintenance ownership |
| codaro | STALE | last main activity 2026-06; review release/CI state |
| hyperframes | STALE | last release activity 2026-06; review maintenance ownership |
| kordoc | STALE | publish workflow intentionally removed; release process needs explicit gate |
| Hermes-Agent_One-Click_Kit | STALE | last main activity 2026-06; refresh or archive |
| joylab-html-tool | BROKEN | stale validation PR replaced and common Release Gate adopted; dedicated Windows/Tauri build validation still needs an executable PR-triggered gate |
| joylab-vercel-site | HEALTHY | common Release Gate caller adopted |
| onboaring | EMPTY | size 0 |
| on_0720 | EMPTY | size 0 |
| masterplan_0722 | EMPTY | size 0 |
| desktop-tutorial | EMPTY | size 0 |
| joylab_ai_coach_tutor | EMPTY | size 0 |
| JoyLab_Vibe_Coding_OS_v1.0 | HEALTHY | engineering-standard work + common Release Gate caller |
| joylab-knowledge-os | ACTIVE | Gold generator bug fixed; D2S CI GREEN; common Release Gate adopted |
| joylab-cs-adaptive-learning | HEALTHY | structured-output compatibility fix + common Release Gate |
| joylab-ai-voice-benchmark | ACTIVE | evidence-foundation/backend CI GREEN + common Release Gate |
| JoyLab-Book-Mining | HEALTHY | Capture Engine V0.2 + regression workflow + common Release Gate |
| joylab-core8-engine | ACTIVE | release train recovered: #13, #8, Portfolio Gate successor #29, Intraday successor #30, AI Power successor #31, Gold Registry #32 merged; #1 intentionally HOLD/SPLIT REQUIRED |
| ohbeopseok-ops | HEALTHY | central Release Gate + Repository Control Tower V0.1 operational |
| joylab-product-hub | HEALTHY | common Release Gate caller adopted |
| joylab-etf-intelligence | HEALTHY | CI Standard V1.0 + JoyLab Release Gate GREEN |
| joylab-search-engine | ACTIVE | Trust Layer CI GREEN + JoyLab Release Gate GREEN |
| joylab-cs-accuracy-os | HEALTHY | 84/84 tests + reproducible Windows build evidence + common Release Gate |
| joylab-agent-os | ACTIVE | Vercel adapter repaired; Python 3.11/3.12/3.13 + certification gate GREEN + JoyLab Release Gate GREEN |
| joylab-money-os | ACTIVE | portable EXE build path + common Release Gate |

## Core8 Recovery Ledger

| Change | Result |
|---|---|
| PR #13 Exposure Consolidation | MERGED — `01cef4b...` |
| PR #8 NVDA D+3 | FIXED + GREEN + MERGED — `f55cdcfa...` |
| PR #12 Portfolio Gate | old PR superseded; clean successor #29 GREEN + MERGED — `ccad9bda...` |
| PR #10 Intraday Validation | old PR superseded; clean successor #30 GREEN + MERGED — `923f6ac9...` |
| PR #6 AI Power Rotation | old PR superseded; clean successor #31 GREEN + MERGED — `8c047702...` |
| PR #3 Gold Case Registry | stale PR closed; recovery #32 preserved latest NVDA data, GREEN + MERGED — `52e142ca...` |
| PR #1 Rebalancing mega-PR | HOLD / SPLIT REQUIRED; no force-merge |

## Current priority queue

1. **P0 — joylab-html-tool**: establish a dedicated Windows/Tauri PR-triggered build gate and prove artifact generation.
2. **P1 — core8 PR #1**: inventory 39 unique files and split by rule family; never merge as one mega-PR.
3. **P1 — Control Tower private scope**: add `CONTROL_TOWER_TOKEN` only if full private-repository automation is desired.
4. **P2 — title-triumphs-tool**: regenerate/synchronize `package-lock.json`, then restore strict `npm ci`.
5. **P2 — EMPTY/ARCHIVE group**: archive only after explicit owner review.

## Promotion rule

A repository is release-ready only when:

`CI → Gold Case → Regression → Build → Release Gate`

all required stages are GREEN for the current main-compatible commit. A stale historical GREEN result is not sufficient.
