# Website validation

## 2026-10-27 — Consistent header navigation

- All 10 HTML pages show the same five links in the same order: The app, AI
  workout guide, Changelog, Terms, Privacy. This includes the schema pages and
  archived terms. Current-page highlighting uses `aria-current="page"`.
- All 12 Python tests, both generated-page checks and the new all-page navigation
  check pass. The navigation check first reproduced the missing link on the
  original changelog, and is now part of the required website CI job.
- Chromium verified all 10 pages at 320, 390 and 1440 pixels: consistent labels
  and resolved destinations, no clipped header links or horizontal page overflow,
  HTTP 200 for each header destination and no browser page errors. Keyboard Tab
  navigation followed by Enter opens the AI guide from the changelog.
- The app's legal exporter reproduces the updated legal-page headers, including
  nested archives. Legal text, downloads, hashes and public schema data are
  unchanged. The website work was previewed locally; it has not been deployed.

Browser captures of the changelog header at a 1440-pixel viewport:

![Original changelog header](images/navigation/changelog-before-desktop.png)
![Consistent header including the AI workout guide](images/navigation/changelog-after-desktop.png)

[Phone changelog](images/navigation/changelog-after-phone.png) ·
[Phone archived terms](images/navigation/archived-terms-phone.png)

## Initial changelog

The initial page was checked locally with Python and headless Chromium:

- Four renderer unit tests passed, covering all version anchors, escaped HTML, schema rejection and development date semantics.
- `scripts/build_changelog.py --check` passed for all 14 historical versions plus Unreleased.
- Home, privacy and changelog pages returned HTTP 200 at 320px, 390px and 1280px viewport widths, with no horizontal overflow or browser page errors. Images decoded after scrolling lazy-loaded images into view.
- All 14 version entries were present and the version index navigated to 0.1.0. Phone and desktop changelog screenshots were visually inspected.
- Workflow YAML parsing and `git diff --check` passed.

These checks previewed the feature branch locally. They did not deploy Pages or test live automatic export from the private app repository. The latter requires the owner's cross-repository Actions secret. PR enforcement also requires owner setup; this connection could not write repository rules. See pr-enforcement.md.
