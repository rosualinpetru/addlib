# How to enable Codecov

CI already measures coverage (`pytest --cov`) and uploads `coverage.xml` via the
Codecov action. To make the dashboard and the README badge work, do the
Codecov-side setup once.

## 1. Connect the repository

1. Go to <https://about.codecov.io> and **log in with GitHub**.
2. Install/authorize the **Codecov GitHub App** for `rosualinpetru/addlib`
   (Codecov → *Settings → install the GitHub App*, or accept the prompt on login).
   The repo then appears in your Codecov dashboard.

## 2. Add the upload token (recommended)

Public repos can sometimes upload tokenless, but it is rate-limited and flaky;
a token is the reliable path.

1. In Codecov: open the repo → **Settings → General → Repository Upload Token**,
   copy it.
2. In GitHub: repo → **Settings → Secrets and variables → Actions → New
   repository secret**.
   - Name: `CODECOV_TOKEN`
   - Value: the token from step 1.

The workflow already references it:

```yaml
- uses: codecov/codecov-action@v4
  with:
    files: ./coverage.xml
    token: ${{ secrets.CODECOV_TOKEN }}
    fail_ci_if_error: false
```

## 3. Trigger an upload

Push any commit to `main` (or open a PR). The `Test` job's
`ubuntu-latest / py3.12` matrix entry uploads coverage. After Codecov processes
it:

- the dashboard shows coverage and per-PR diffs, and
- the README badge
  (`https://codecov.io/gh/rosualinpetru/addlib/branch/main/graph/badge.svg`)
  starts rendering the percentage.

## Tuning

Thresholds and the PR comment are configured in
[`codecov.yml`](https://github.com/rosualinpetru/addlib/blob/main/codecov.yml)
(`project`/`patch` targets, ignored files). `fail_ci_if_error: false` keeps a
Codecov outage from breaking CI; flip it to `true` once you rely on the gate.
