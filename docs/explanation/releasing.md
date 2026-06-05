# Releasing

Releases are **tag-triggered and automated** (Phase 5.4). The human does two
things: bump the version and push a tag. CI does the rest — build, sign,
publish — which removes the manual errors that creep into hand-cut crypto-library
releases (forgetting to sign, shipping an unbuilt platform, a mismatched
changelog).

## One-time setup

- **PyPI Trusted Publishing**: register the repo + `release.yaml` workflow as a
  trusted publisher on PyPI (OIDC). No long-lived API token lives in the repo.
- **Branch protection** on `main`: required review, green CI, signed commits.

## Release checklist

1. Ensure `main` is green and the [changelog](https://github.com/rosualinpetru/addlib/blob/main/CHANGELOG.md) `Unreleased`
   section reflects what is shipping.
2. Bump the version in **both** places that must agree:
   - `pyproject.toml` → `version`
   - `c/include/add/add.h` → `ADDLIB_VERSION_*` / `ADDLIB_VERSION_STRING`
   (`test_version_consistency` and `test_version_symbol` fail if they drift.)
3. Move `Unreleased` → `[X.Y.Z] — DATE` in the changelog; add the compare link.
4. Commit (`-s`, signed): `git commit -S -s -m "chore(release): vX.Y.Z"`.
5. Tag and push: `git tag -s vX.Y.Z -m "vX.Y.Z" && git push --tags`.

## What the tag triggers (`release.yaml`)

1. **Build** wheels (cibuildwheel: manylinux, macOS incl. Apple Silicon,
   Windows) and an sdist; each wheel is import-smoke-tested.
2. **SBOM** (CycloneDX) generated for the release.
3. **Provenance** attestation (SLSA / GitHub artifact attestations) for every
   artifact.
4. **Publish** to PyPI via Trusted Publishing.
5. **Sign** artifacts with Sigstore and attach signatures + SBOM + checksums to
   a **GitHub Release**, with notes derived from Conventional Commits.

## Cadence

Release when there is something worth releasing (not on a rigid clock) — but
always be able to ship a **security patch fast** (the disclosure runbook drives
those out-of-band).

## Distribution channels

- **PyPI** — wheels + sdist, from day one.
- **GitHub Releases** — canonical home for signed artifacts, SBOM, checksums.
- **conda-forge** — add a feedstock around the first stable release; much of the
  scientific-Python audience lives in conda and won't build native extensions by
  hand. (Demand-driven; not set up yet.)
- **vcpkg / Conan** for `libadd` — only if/when C consumers ask. Don't pre-build.
