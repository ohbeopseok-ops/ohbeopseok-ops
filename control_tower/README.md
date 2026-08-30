# JoyLab Repository Control Tower V0.1

A zero-dependency GitHub repository health scanner for the JoyLab account.

## Outputs

- `reports/repository-health.json` — machine-readable registry.
- `reports/repository-health.md` — operator dashboard.

## Automatic schedule

The workflow runs every day at **07:15 KST** and can also be triggered manually.

## Private repositories

Create an Actions secret named `JOYLAB_GITHUB_TOKEN` in this controller repository.
Use a fine-grained token with **read-only metadata + Actions read** access to the JoyLab repositories.

If the secret is absent, V0.1 safely falls back to public repository discovery and records the scope as `public-only` instead of pretending private repositories were checked.

## State priority

`ARCHIVE → EMPTY → BROKEN → ACTIVE → STALE → HEALTHY`

A failed latest visible workflow blocks promotion even when the repository is recent.
