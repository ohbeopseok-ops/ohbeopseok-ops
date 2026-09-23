# JoyLab Repository Governance V1.0

Effective date: 2026-09-23  
Scope: all repositories owned by `ohbeopseok-ops`

## 1. Purpose

JoyLab repositories are managed as a portfolio, not as isolated experiments. Every repository must have one portfolio, one business owner, one purpose, and one health state.

Source of truth: `control_tower/repository-governance.json`

## 2. Portfolio model

| Portfolio | Meaning | Creation rule | Exit rule |
|---|---|---|---|
| Core | Shared infrastructure or system of record used by multiple JoyLab products | requires clear cross-project dependency | split only when ownership and interface are stable |
| Product | A user-facing or independently releasable product/tool | must have owner, README, test/build path | move to Archive after explicit owner decision |
| Experiment | Time-boxed prototype or hypothesis test | define success/fail condition before implementation | promote to Product/Core or archive |
| Reference | Imported/reference code kept for learning or comparison | no implicit production dependency | archive when no longer referenced |
| Archive | Abandoned, superseded, empty legacy, or one-off repository | no new product work | GitHub archive after owner review |

## 3. Health model

Control Tower V0.2 emits exactly six health states:

- **GREEN** — no known blocker; critical workflow state is clear.
- **YELLOW** — operational automation needs attention, but critical release/CI gates are not known broken.
- **RED** — latest critical workflow failed.
- **STALE** — no push for more than 60 days.
- **EMPTY** — no committed project payload.
- **ARCHIVE** — governance portfolio is Archive or the GitHub repository is archived.

Health and portfolio are independent. A Product can be RED; a Reference can be STALE; an Archive remains ARCHIVE.

## 4. Repository creation gate

A new repository is allowed only when all five fields are decided before creation:

1. **Goal** — what outcome requires a separate repository?
2. **Portfolio** — Core / Product / Experiment / Reference / Archive.
3. **Owner** — who decides scope and lifecycle?
4. **Promotion gate** — what proves it is usable?
5. **Sunset rule** — when is it merged, archived, or deleted?

If the proposed work is only a feature of an existing Core/Product repository, create a branch or package there instead of a new repository.

## 5. Promotion gate

For releasable Core/Product repositories, the target sequence is:

`CI → Gold Case → Regression → Build → Release Gate`

Not every repository needs every stage, but skipped stages must be intentional and documented. Historical GREEN does not certify a newer commit.

## 6. Current 44-repository portfolio

The machine-readable assignment is maintained in `control_tower/repository-governance.json`.

### Core

`ohbeopseok-ops`, `joylab-command-center`, `joylab-content-os`, `joylab-core8-engine`, `joylab-knowledge-os`, `joylab-notes`, `joylab-portfolio-os`, `joylab-product-hub`, `joylab-publishing-os`, `joylab-search-engine`

### Product

`cs-ops-skills`, `joylab-agent-os`, `joylab-ai-voice-benchmark`, `JoyLab-Book-Mining`, `joylab-cs-accuracy-os`, `joylab-cs-adaptive-learning`, `joylab-etf-intelligence`, `joylab-html-tool`, `joylab-moment15-ios`, `joylab-money-os`, `JoyLab-SEO`, `joylab-vercel-site`, `JoyLab_Vibe_Coding_OS_v1.0`, `leaderdesk`, `senior-toilet-finder`, `title-triumphs-tool`

### Experiment

`-joylab-plan-ai`, `basic-comics`, `joylab_ai_coach_tutor`, `onboaring`

### Reference

`codaro`, `dartlab`, `Hermes-Agent_One-Click_Kit`, `hyperframes`, `kordoc`

### Archive

`-`, `copy-of-ai-meet`, `desktop-tutorial`, `https-github.com-uxjoseph-ppt_team_agent`, `masterplan_0722`, `meeting`, `on_0720`, `risk-zero`, `sales-point`

Total: **44**

## 7. Operating cadence

- Daily: Control Tower V0.2 scans all governed repositories.
- Weekly: review RED/YELLOW and Experiments older than their intended time box.
- Monthly: review STALE and Archive candidates.
- Quarterly: confirm that Core boundaries still match real dependencies.

## 8. No-auto-destruction rule

Control Tower may classify and report. It must not automatically delete, archive, rename, or merge repositories. Lifecycle mutations require explicit owner review.
