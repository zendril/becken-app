# Working on the Becken website

Read README.md first. This is the public static GitHub Pages website; the Android source remains private in `zendril/becken`.

- Fetch origin and inspect open PRs before editing. Use a dedicated feature branch from current main, preserving other sessions' changes. Every change, including documentation and generated content, goes through a PR.
- Do not push directly to main, force-push shared branches, or merge without explicit owner authorization. Before requesting merge, incorporate current main and rerun relevant checks. Reserve `automation/changelog` for the app's publication workflow.
- GitHub rules enforce this on the server only after the owner configures them. See `docs/pr-enforcement.md`; AGENTS.md alone cannot block a push.
- Preserve the existing Momentum logo, orange/midnight palette, accessible navigation and responsive layouts. Do not introduce analytics, third-party fonts or browser scripts without a product requirement.
- `changelog/releases.json` is a reviewed export from the private app's canonical file. Update it there first and export it. Do not independently rewrite the website's history. Never infer a release date from a commit date.
- Generate `changelog/index.html` with `python3 scripts/build_changelog.py --write`; do not edit it directly. Run `python3 scripts/build_changelog.py --check` and `python3 -m unittest discover -s scripts -p 'test_*.py'` before committing.
- Preview affected pages at phone and desktop widths. Document actual checks in the PR. Pages serves committed files from main; no production Python build step is required.
- Only public prose and approved assets belong here. Never add private app source, credentials, personal training records or internal changelog provenance.
