# Becken website

Minimal static landing page and Privacy Policy for **becken.app**. No build step, JavaScript, third-party fonts, or analytics. The Android app's source stays in the separate private repository.

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

The public policy URL will be **https://becken.app/privacy/**. Add it in Play Console and in the Android app as part of release setup. Confirm that `support@becken.app` receives email; hosting the site does not provision email.

Committing these files does not itself enable Pages or change domain DNS.

## Content maintenance

- Both Play buttons in `index.html` target `https://play.google.com/store/apps/details?id=app.becken.android`, based on the app's selected package ID. Access is currently limited to invited testers; send testers the Play Console opt-in link separately. The live listing was not verified from this environment. Update the two availability notes when public distribution begins.
- `privacy/index.html` reflects the app's current local storage and manual backups, disabled automatic Drive integration, and this static site's hosting. Reconcile it with any future changes to billing, analytics, cloud features, or support handling before releasing them.
- Branding uses the implemented Momentum logo and palette from `zendril/becken/docs/brand.md`: orange `#FF7A1A`, midnight `#081722`, paper `#FFF8F3`, and deep orange `#A44000`. It does not claim to recover the original concept artwork.
- Logo and social image are copied from `assets/branding/becken-momentum.svg` and `.png` in the app repo.
- The three original screenshot PNGs are from `assets/play-store-examples/dark/` at app commit `92b1ac77df4a113902fbfd9851e7e888849eb07b`. They show sample data in Becken 0.6.1, captured on an Android 11 emulator at 1280 × 2856; they are not physical Pixel captures or screenshots of the 0.6.2 release. Pixels are unmodified, with decorative borders applied only by website CSS.

No app source, credentials, or personal training records belong in this public repository.
