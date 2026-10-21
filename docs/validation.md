# Changelog validation

The initial page was checked locally with Python and headless Chromium:

- Four renderer unit tests passed, covering all version anchors, escaped HTML, schema rejection and development date semantics.
- `scripts/build_changelog.py --check` passed for all 14 historical versions plus Unreleased.
- Home, privacy and changelog pages returned HTTP 200 at 320px, 390px and 1280px viewport widths, with no horizontal overflow or browser page errors. Images decoded after scrolling lazy-loaded images into view.
- All 14 version entries were present and the version index navigated to 0.1.0. Phone and desktop changelog screenshots were visually inspected.
- Workflow YAML parsing and `git diff --check` passed.

These checks previewed the feature branch locally. They did not deploy Pages or test live automatic export from the private app repository. The latter requires the owner's cross-repository Actions secret. PR enforcement also requires owner setup; this connection could not write repository rules. See pr-enforcement.md.
