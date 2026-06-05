# Releasing

Releases are **tag-triggered and automated**. The human does two
things: bump the version and push a tag. CI does the rest — build, sign,
publish — which removes the manual errors that creep into hand-cut native-extension
releases (forgetting to sign, shipping an unbuilt platform, a mismatched
changelog).

## One-time setup

- **PyPI Trusted Publishing**: register the repo + `release.yaml` workflow as a
  trusted publisher on PyPI (OIDC). No long-lived API token lives in the repo.
- **Branch protection** on `main`: required review, green CI, signed commits.

## Release checklist

1. Ensure `main` is green.
2. Bump the version with one command:
   ```bash
   make bump V=X.Y.Z
   ```
   This writes the single source of truth — the top-level `VERSION` file (the
   Python distribution version) — and the C library version in
   `c/include/add/add.h`. A test (`test_version_consistency`) fails if the two
   ever drift.
3. Update the changelog (`make changelog` regenerates it from Conventional
   Commits via git-cliff; or hand-edit `CHANGELOG.md`).
4. Commit (`-s` for DCO): `git commit -s -m "chore(release): vX.Y.Z"`.
5. Tag and push: `git tag -a vX.Y.Z -m "vX.Y.Z" && git push origin vX.Y.Z`.

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
- **conda-forge** — much of the scientific-Python audience lives in conda and
  won't build native extensions by hand. A ready-to-adapt recipe is in
  [`recipe/meta.yaml`](https://github.com/rosualinpetru/addlib/blob/main/recipe/meta.yaml);
  submission steps are in [`recipe/README.md`](https://github.com/rosualinpetru/addlib/blob/main/recipe/README.md). (Demand-driven; not yet submitted.)
- **vcpkg / Conan** for `libadd` — only if/when C consumers ask. Don't pre-build.
