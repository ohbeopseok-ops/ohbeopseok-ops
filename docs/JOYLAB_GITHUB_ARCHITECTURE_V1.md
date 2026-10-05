# JoyLab GitHub Architecture V1.0

## Objective

Keep `ohbeopseok-ops` as the single human Super Admin identity and operate production work through business-unit GitHub Organizations.

## Target topology

- `ohbeopseok-ops`
  - Personal identity
  - Super Admin / break-glass owner
  - Playground, forks, temporary PoCs

- `joylab-research`
  - Publishing, research, SEO, investment intelligence
  - Initial repos:
    - joylab-publishing-os
    - joylab-vercel-site
    - joylab-research-factory
    - JoyLab-SEO
    - joylab-etf-intelligence
    - joylab-core8-engine
    - joylab-money-os
    - joylab-portfolio-os
    - joylab-search-engine
    - JoyLab-Book-Mining

- `joylab-labs`
  - AI, agents, apps, automation, media systems
  - Initial repos:
    - joylab-agent-os
    - joylab-ai-company-os
    - joylab-command-center
    - joylab-motion-factory
    - joylab-video-factory
    - joylab-shortform-engine
    - joyclip
    - joylab-product-hub
    - joylab-plan-ai
    - joylab-ai-voice-benchmark
    - joylab-moment15-ios

- `leaderdesk`
  - LeaderDesk and CS operations products
  - Initial repos:
    - leaderdesk
    - leaderdesk-people-os
    - cs-ops-skills
    - joylab-cs-accuracy-os
    - joylab-cs-adaptive-learning
    - joylab_ai_coach_tutor

## Governance rules

1. `ohbeopseok-ops` remains Owner of every Organization.
2. Production repositories are owned by Organizations, not by extra personal accounts.
3. Repository migration is wave-based; no bulk move.
4. Secrets are scoped to the minimum repository or environment necessary.
5. Production deploys use protected environments and explicit release gates.
6. Heavy CI moves to labeled self-hosted runners where appropriate.
7. Scheduled workflows are consolidated and reviewed for cost/noise.
8. Every migration must pass Clone, PR, Actions, Secrets, Deploy, Release, and rollback checks before the next repository moves.

## Runner model

### GitHub-hosted Ubuntu
Use for fast PR gates:
- lint
- typecheck
- unit tests
- schema/content validation
- small smoke tests

### JoyLab Mac self-hosted
Suggested labels:
- self-hosted
- macOS
- ARM64
- joylab

Use for:
- AI benchmarks
- Research Factory heavy jobs
- browser/visual QA
- Motion/Video Factory
- large audits

### LeaderDesk Windows self-hosted
Suggested labels:
- self-hosted
- Windows
- X64
- leaderdesk

Use for:
- Windows packaging
- installer/update tests
- migration tests
- backup/restore tests
- GOLD release candidates

## Migration order

### Wave 1 — JoyLab Labs pilot
1. joylab-agent-os
2. joylab-ai-company-os
3. joylab-video-factory
4. joylab-motion-factory
5. joyclip

### Wave 2 — LeaderDesk
1. leaderdesk
2. leaderdesk-people-os
3. related CS repos

### Wave 3 — Research / Production
1. joylab-research-factory
2. joylab-vercel-site
3. joylab-publishing-os

`joylab-publishing-os` moves last because it currently has a large workflow surface and production integrations.

## Gold Test

A moved repository is GREEN only if:
- remote clone/fetch works from current machines
- existing branches and tags remain available
- open PR/issue links redirect correctly
- Actions trigger successfully
- required secrets/environments exist
- external integrations point to the new owner/repo
- deploy works
- rollback path is documented
- release/update URLs are validated where applicable

