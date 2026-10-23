# Becken website

Minimal static landing page, changelog, Terms of Service and Privacy Policy for **becken.app**. No production build step, JavaScript, third-party fonts, or analytics. The Android app's source stays in the separate private repository.

## Preview

Run `python3 -m http.server 8000` from this directory and visit http://localhost:8000. The Privacy Policy is at `/privacy/`. Relative links also support the GitHub Pages project URL before the custom domain is active.

## Publish with GitHub Pages

1. Open **Settings → Pages** in this repository.
2. Under **Build and deployment**, choose **Deploy from a branch**, then **main** and **/ (root)**, and save.
3. Set the custom domain to `becken.app` (also recorded in `CNAME`).
4. At your domain provider, configure these apex DNS records:

   | Type | Host | Value |
   | --- | --- | --- |
   | A | @ | 185.199.108.153 |
   | A | @ | 185.199.109.153 |
   | A | @ | 185.199.110.153 |
   | A | @ | 185.199.111.153 |
   | CNAME | www | zendril.github.io |

   Remove conflicting website A/AAAA records, but preserve email MX/TXT records. Optional IPv6 and domain verification instructions are in [GitHub's custom-domain documentation](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site).
5. When GitHub finishes its DNS check and certificate provisioning, enable **Enforce HTTPS**. `.app` domains require HTTPS.

The public policy URL is **https://becken.app/privacy/**. Use it in Play Console and the Android app as part of release setup. Hosting the site does not provision a support or privacy inquiry channel.

Committing these files does not itself enable Pages or change domain DNS.

## Content maintenance

- Lead with **Free to use. No subscription. Fully offline.** in the landing page and search/social descriptions. Offline use includes routines, workout logging, history, and local backup/restore. Optional cloud storage needs a connection; do not imply cloud transfers work offline.
- Both Play buttons in `index.html` target `https://play.google.com/store/apps/details?id=app.becken.android`, based on the app's selected package ID. Access is currently limited to invited testers; send testers the Play Console opt-in link separately. The live listing was not verified from this environment. Update the two availability notes when public distribution begins.
- `privacy/index.html` reflects the app's current local storage and manual backups, disabled automatic Drive integration, and this static site's hosting. Reconcile it with any future changes to billing, analytics, cloud features, or support handling before releasing them.
- Branding uses the implemented Momentum logo and palette from `zendril/becken/docs/brand.md`: orange `#FF7A1A`, midnight `#081722`, paper `#FFF8F3`, and deep orange `#A44000`. It does not claim to recover the original concept artwork.
- Logo and social image are copied from `assets/branding/becken-momentum.svg` and `.png` in the app repo.
- The three original screenshot PNGs are from `assets/play-store-examples/dark/` at app commit `92b1ac77df4a113902fbfd9851e7e888849eb07b`. They show sample data in Becken 0.6.1, captured on an Android 11 emulator at 1280 × 2856; they are not physical Pixel captures or screenshots of the 0.6.2 release. Pixels are unmodified, with decorative borders applied only by website CSS.

No app source, credentials, or personal training records belong in this public repository.

## Legal document maintenance

Terms, privacy and downloaded text are reviewed exports from the app's canonical
versioned legal sources. Do not independently rewrite `terms/`, `privacy/` or
`legal/documents.json`. From the app checkout, run
`python3 scripts/legal.py --write --base origin/main --export-site
/path/to/website`, then use `--check` with the same arguments. The generator
protects terms text already merged in this repository's `origin/main`; fetch
that branch before exporting. Retain every published terms version and archive
index link. Run the website Python tests and preview phone/desktop/print layouts.

The site displays the terms and exercise-risk notice; it does not record assent
from visits or download clicks. The Android app asks for explicit agreement.
Interactive exercise features on the website would require their own acceptance
flow. The static page must not claim that a footer alone records agreement or
that all possible liability is excluded.

The current documents describe the individual operating Becken under zendril.dev
in Delaware. A personal name and email are omitted at the owner's request, and
there is no invented contact form or email-reporting action. The generated pages,
downloadable text, public legal JSON and terms archive use that chosen wording.

Google Play separately requires a reachable listing support email and a privacy
contact or inquiry mechanism. The current contact-free policy is not declared
Play-compliant; establish a verified inquiry route before relying on it for Play
publication. A working inquiry mechanism can avoid printing an email in the
policy. See [Google's support requirements](https://support.google.com/googleplay/android-developer/answer/113477?hl=en)
and [User Data policy](https://support.google.com/googleplay/android-developer/answer/10144311?hl=en).
No store contact setting is changed by these website files.

## Changelog maintenance

The public history is at `https://becken.app/changelog/` after the changelog PR is merged. Canonical notes live in the private app repository's `changelog/releases.json`; this repository contains only a reviewed export. The app's publisher opens or updates a website PR; merging it publishes through the existing Pages configuration. With [auto-merge and required checks configured](docs/pr-enforcement.md), the publisher requests auto-merge for generated changelog-only PRs after the `site` check passes. Other website PRs and app PRs remain manual. Missing setup leaves the generated PR open for manual review.

From the app checkout, export to this checkout with `python3 scripts/changelog.py --export-site /path/to/website`. Then run here:

```sh
python3 scripts/build_changelog.py --write
python3 scripts/build_changelog.py --check
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 -m http.server 8000
```

Review `/changelog/`, the home page and `/privacy/` at phone and desktop widths. Commit the exported JSON and generated HTML on a feature branch, then raise a PR. Python runs during maintenance/CI; visitors receive static HTML. Don't edit generated HTML or diverge from the app's canonical notes. Development history does not imply public availability; only verified releases receive dates.

The app workflow needs a `SITE_CHANGELOG_TOKEN` secret restricted to this website repository (Contents and Pull requests write). Configure it in the private app repository, never here or in committed files. Until configured, use the manual export above. Details are in the private app's `docs/changelog.md`.

Every change must go through a PR. See [AGENTS.md](AGENTS.md) and [server-side enforcement setup](docs/pr-enforcement.md). The rule configuration still needs owner action; this session's integration could not administer rules.
