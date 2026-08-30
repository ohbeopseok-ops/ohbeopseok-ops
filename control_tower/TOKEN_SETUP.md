# JoyLab Control Tower — 35 Repository Token Setup

## Goal

Upgrade discovery from **public-only** to **authenticated-owner** so Control Tower V0.2 can inspect all JoyLab public and private repositories.

## Secret name

`JOYLAB_GITHUB_TOKEN`

The workflow is already wired to this exact repository secret name.

## Recommended token type

Use a **Fine-grained personal access token** owned by the JoyLab GitHub account.

### Repository access

Choose **All repositories** for the account if the goal is automatic coverage of current and future JoyLab repositories.

If you choose **Selected repositories**, select all 35 current JoyLab repositories and remember that newly created repositories will not be covered until added.

### Repository permissions

Grant only:

- **Metadata: Read-only** — mandatory/basic repository discovery.
- **Actions: Read-only** — read workflow runs and conclusions.

No Contents write, Administration, Secrets, Pull Requests, or Issues permission is required on this PAT.

## Why Issue write is not granted to the PAT

BROKEN issues are centralized in `ohbeopseok-ops/ohbeopseok-ops`.

The workflow's built-in `GITHUB_TOKEN` has:

- `contents: write` — publish generated health reports.
- `issues: write` — create/refresh/reopen/close Control Tower issues.

This deliberately separates:

- **Cross-repository read credential** = `JOYLAB_GITHUB_TOKEN`
- **Controller mutation credential** = workflow `GITHUB_TOKEN`

## One-time GitHub UI step

In `ohbeopseok-ops/ohbeopseok-ops`:

1. Open **Settings → Secrets and variables → Actions**.
2. Choose **New repository secret**.
3. Name: `JOYLAB_GITHUB_TOKEN`.
4. Paste the fine-grained token value.
5. Save.
6. Run **JoyLab Repository Control Tower** manually once.

## Expected validation

The generated `reports/repository-health.json` should show:

```json
{
  "scope": "authenticated-owner"
}
```

and the repository count should match the current owned repository count rather than public repositories only.

## Rotation

Use a finite expiry. Rotate the token before expiration. If it expires, Control Tower safely falls back to `public-only` rather than claiming private repositories were scanned.
