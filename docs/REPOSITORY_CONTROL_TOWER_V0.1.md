# JoyLab Repository Control Tower V0.1

## Purpose

Continuously convert GitHub repository and Actions evidence into an auditable health registry.

## Inputs

- repositories owned by `ohbeopseok-ops`
- repository size / archived / pushed_at metadata
- latest GitHub Actions workflow runs

## States

- `BROKEN`: latest completed Actions run has a blocking failure conclusion
- `ACTIVE`: repository has recent push activity within 14 days and no known blocking failure
- `HEALTHY`: non-empty, non-stale, no known blocking failure
- `STALE`: no push for more than 60 days
- `EMPTY`: repository size is 0
- `ARCHIVE`: repository is already archived

## Hard rules

1. V0.1 never deletes or archives repositories.
2. Historical GREEN never certifies a newer commit.
3. BROKEN outranks activity recency.
4. EMPTY repos do not receive synthetic CI work.
5. Generated evidence is committed so classification changes are reviewable in Git history.

## Outputs

- `control_tower/repository-health.json`
- `GITHUB_HEALTH_REGISTRY_AUTO.md`

## Schedule

Daily at 07:17 KST (22:17 UTC previous day), plus manual dispatch.

## V0.2 candidates

- open PR age / mergeability
- branch divergence
- required-check coverage
- deployment status
- stale PR auto-labeling
- alert-only-on-state-transition
