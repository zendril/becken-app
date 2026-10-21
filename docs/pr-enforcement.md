# Require pull requests

All website changes must use a feature branch and PR. To enforce this, the owner should open [Settings → Rules → Rulesets](https://github.com/zendril/becken-app/settings/rules) and import [github-main-ruleset.json](github-main-ruleset.json) through the New ruleset menu.

The active rule targets main, requires a PR with resolved conversations, blocks deletion and force pushes, and has no bypass actors. Zero required approvals lets the solo owner merge their own PR; this still requires a PR. After the `site` CI check has run, add it as a required status check if desired.

This work could not enable the rule: GitHub returned `403: Resource not accessible by integration` for administration writes. The public repository supports rulesets, but the owner must apply the settings or provide an integration with repository administration permission. Existing classic protection could not be inspected. Documentation and CI alone do not prohibit direct pushes.

Confirm the rule is Active and applies to main, with no bypass list. Do not test by pushing a dummy commit to main. Administrators who can edit rules can disable them. Publication automation must also submit a PR and wait for an authorized merge.
