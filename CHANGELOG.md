# Changelog

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning: [SemVer](https://semver.org/).

## [Unreleased]

### Changed
- Repository renamed from `cs2-callouts` (old GitHub URLs redirect).

## [1.0.0] - 2026-11-10

First public release.

### Added
- Callouts for 10 maps (Dust II, Mirage, Inferno, Nuke, Overpass, Ancient, Anubis, Train, Vertigo, Cache) with names in en, ru, de and fr, positioned on the Boltobserv radars (the radars themselves are not included).
- `schematic/`: a licence-clean alternative with our own schematic images and a reproducible build pipeline.
- Tests for the data schema and for reproducibility of `callouts.json`; CI and a release workflow that publishes a zip with checksums.

### Changed
- `schematic/scripts/build.py` finds its `data/` relative to the repository, so it can be run from anywhere.
