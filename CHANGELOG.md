# Changelog

Notable changes to ix-recipes. Skills are versioned individually (semver in each skill's frontmatter); the plugin version lives in `dist/.claude-plugin/plugin.json`. Format inspired by [Keep a Changelog](https://keepachangelog.com).

## 2026-10-14 — plugin 1.0.0

### Added — repository created from ix-skills

48 skills moved from [ix-skills](https://github.com/amiel-35/ix-skills) (commit `9229d48`) with their git history: HR, legal, finance, sales and procurement, product, tech, data. `note-strategique` and `offer-comparison` come along as standalone skills, to be rewritten as workflows chaining ix-skills atoms.

### Changed

- `financial-narrative` 1.1.1: no longer points to `data-storytelling`, which is not carried over.
- `ticket-triage` 1.1.1: no longer points to `retrospective`, which is not carried over.
