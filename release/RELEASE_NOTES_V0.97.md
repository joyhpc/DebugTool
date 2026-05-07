# Release Notes - V0.97 Seed Intake Structure

Status: founder-pilot candidate. Not team-wide pilot ready. Not V1.0.

## Goal

V0.97 clarifies how user-provided articles, public posts, and vendor notes enter the skill. These sources should first become `pattern_bundle` assets, not validated `case_record` assets.

## Main Changes

- Added `pattern_bundle` asset type and `PBU-` ID prefix.
- Added source types: `public_article`, `public_forum`, `vendor_app_note`, `user_provided_article`.
- Moved the power-debug 10-pitfalls seed into `assets/pattern_bundles/PBU-POWER-DEBUG-10-PITFALLS-SEED.yaml`.
- Kept case records reserved for single, evidence-backed debug cases.
- Updated README, SKILL, schema, linter, regression version, and changelog.

## Known Limits

- Regression remains structural, not LLM-backed behavior testing.
- Pattern bundles can influence prioritization, but they must not override current measurements or safety gates.
- Public/user-provided material is seed evidence until corroborated by real runs.
