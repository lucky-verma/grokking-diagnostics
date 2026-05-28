# Public Release Checklist

Use this checklist before refreshing the public artifact repo or tagging a
release.

- [x] State the artifact contract: diagnostics package, aggregate-backed figures,
      provenance manifests, Lean checks, and companion dataset.
- [x] Keep the README explicit that full retraining and one-command regeneration
      of every figure are not claimed.
- [x] Include machine-readable citation metadata in `CITATION.cff`.
- [x] Include a numerical verifier for the shipped aggregate surface.
- [x] Include `Makefile` shortcuts for install, optional figure/data
      dependencies, validation, figures, tests, dataset aggregate download, and
      Lean checks.
- [x] Include CI for Python tests, lint, numerical verification, and Lean.
- [x] Link the public Hugging Face dataset.
- [ ] Tag the first public GitHub release.
- [ ] Optional: mint an archival software/data DOI after the first release tag.
- [ ] Optional: publish a minimal notebook or script that computes the attention
      diagnostics on a toy transformer forward pass.
