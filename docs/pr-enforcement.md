# Require pull requests

All website changes must use a feature branch and PR. To enforce this, the owner should open [Settings → Rules → Rulesets](https://github.com/zendril/becken-app/settings/rules) and import [github-main-ruleset.json](github-main-ruleset.json) through the New ruleset menu.

The active rule targets main, requires a PR with resolved conversations, blocks deletion and force pushes, and has no bypass actors. Zero required approvals lets the solo owner merge their own PR; this still requires a PR. The template requires the `site` check from GitHub Actions and requires the PR branch to be up to date. This check is mandatory for automatic changelog merging. If updating an existing ruleset, add these settings there instead of importing a duplicate.

This work could not enable the rule: GitHub returned `403: Resource not accessible by integration` for administration writes. The public repository supports rulesets, but the owner must apply the settings or provide an integration with repository administration permission. Existing classic protection could not be inspected. Documentation and CI alone do not prohibit direct pushes.

Confirm the rule is Active and applies to main, with no bypass list. Do not test by pushing a dummy commit to main. Administrators who can edit rules can disable them. Publication automation also submits a PR. The owner authorized auto-merge for generated changelog-only PRs; app PRs and other website PRs remain manual. In Settings → General → Pull Requests, enable **Allow auto-merge** and **Allow squash merging**. The app publisher then requests auto-merge only for `automation/changelog` PRs modifying `changelog/releases.json` and `changelog/index.html`, after verifying the expected commit and required rules. GitHub waits for all required checks/reviews; it may merge immediately if they already pass. No bypass actor is needed. A stale branch needs updating (rerun the publisher), and failing checks must be fixed. This repository setting does not automatically merge unrelated PRs.

## Activation

Merge the configuration/documentation PRs manually, apply the settings above, and run **Propose website changelog update** on `main` in the app repository. Existing generated PRs can be picked up by that run. A successful merge triggers the normal Pages deployment. Missing auto-merge/ruleset setup leaves the generated PR manual with a warning. The existing publication token needs only Contents and Pull requests read/write; no new token or Administration permission is required for routine publication.
