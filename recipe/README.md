# conda-forge recipe

[`meta.yaml`](meta.yaml) is a ready-to-adapt conda-forge recipe for `addlib`.
It is **not** published automatically — conda-forge packages live in their own
feedstock repositories and are added by a reviewed PR.

## How to actually get on conda-forge

1. Publish the release to **PyPI** first (conda-forge builds from the PyPI sdist).
2. Fork **<https://github.com/conda-forge/staged-recipes>**.
3. Copy this `meta.yaml` to `recipes/addlib/meta.yaml` in your fork and fill in
   the `sha256` of the published sdist:
   ```bash
   openssl dgst -sha256 dist/addlib-<version>.tar.gz
   ```
4. Open a PR to `staged-recipes`. The conda-forge bots lint/build it; a reviewer
   merges it, which creates an `addlib-feedstock` repository.
5. After that, **version bumps are automated** — the conda-forge bot opens a PR
   on the feedstock whenever a new PyPI release appears. You just review/merge.

> This experiment publishes to **TestPyPI**, which conda-forge does not build
> from, so this recipe is provided as a template rather than a live submission.
