#!/usr/bin/env python3
"""Asset linter for Debug Decision Tree Skill.

This is still a structural/static linter. It verifies schema consistency,
reference integrity, basic enum values, and a few quality gates that prevent
empty-but-valid assets from entering the library.
"""

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
ids: dict[str, Path] = {}
errors: list[str] = []
warnings: list[str] = []

ALLOWED_TYPES = {"link_model", "signature", "case_record", "pattern_bundle", "debug_principle"}
ALLOWED_STATUS = {
    "draft",
    "candidate",
    "validated_seed",
    "validated_real_case",
    "generalized",
    "deprecated",
}
ALLOWED_SAFETY = {"S0", "S1", "S2", "S3"}
ALLOWED_WEIGHT = {"high", "medium", "low"}
ALLOWED_CONFIDENCE = {"low", "medium", "high"}
ALLOWED_SOURCE_TYPE = {
    "seed",
    "real_case",
    "authoritative_doc",
    "project_doc",
    "hypothesis",
    "public_article",
    "public_forum",
    "vendor_app_note",
    "user_provided_article",
}
ALLOWED_REF_RELATION = {
    "derived_from",
    "refines",
    "counterexample_of",
    "parent_of",
    "supports",
    "depends_on",
}
ID_PREFIX = {
    "link_model": "LM-",
    "signature": "SIG-",
    "case_record": "CASE-",
    "pattern_bundle": "PBU-",
    "debug_principle": "DP-",
}


def fail(path: Path, msg: str) -> None:
    errors.append(f"{path}: {msg}")


def warn(path: Path, msg: str) -> None:
    warnings.append(f"{path}: {msg}")


def as_list(value: object) -> list[Any]:
    return value if isinstance(value, list) else []


asset_paths = sorted((ROOT / "assets").rglob("*.yaml"))
for path in asset_paths:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    aid = data.get("id")
    atype = data.get("asset_type")
    title = data.get("title", "")

    if not aid:
        fail(path, "missing id")
    elif aid in ids:
        fail(path, f"duplicate id also in {ids[aid]}")
    else:
        ids[aid] = path

    if atype not in ALLOWED_TYPES:
        fail(path, f"invalid asset_type {atype}")
    elif aid and not str(aid).startswith(ID_PREFIX[atype]):
        fail(path, f"id should start with {ID_PREFIX[atype]} for {atype}")

    for key in [
        "title",
        "version",
        "domain",
        "applicability",
        "use_when",
        "do_not_use_when",
        "confidence",
        "safety_level",
        "source",
        "status",
    ]:
        if key not in data:
            fail(path, f"missing {key}")

    if data.get("status") not in ALLOWED_STATUS:
        fail(path, f"invalid status {data.get('status')}")

    if data.get("safety_level") not in ALLOWED_SAFETY:
        fail(path, f"invalid safety_level {data.get('safety_level')}")

    if data.get("confidence") not in ALLOWED_CONFIDENCE:
        fail(path, f"invalid confidence {data.get('confidence')}")

    if "destructive" in data and not isinstance(data.get("destructive"), bool):
        fail(path, "destructive must be boolean")

    source = data.get("source") or {}
    if not isinstance(source, dict):
        fail(path, "source must be a mapping")
    elif source.get("type") not in ALLOWED_SOURCE_TYPE:
        fail(path, f"invalid source.type {source.get('type')}")

    use_when = as_list(data.get("use_when"))
    if not use_when:
        fail(path, "use_when must be non-empty")
    for idx, cond in enumerate(use_when, start=1):
        if not isinstance(cond, dict):
            fail(path, f"use_when[{idx}] must be a mapping")
            continue
        condition = str(cond.get("condition", "")).strip()
        weight = cond.get("weight")
        if not condition:
            fail(path, f"use_when[{idx}] missing condition")
        if weight not in ALLOWED_WEIGHT:
            fail(path, f"use_when[{idx}] invalid weight {weight}")
        if atype == "link_model" and condition.lower() == str(title).strip().lower():
            fail(path, "link_model use_when condition must be triggering symptoms, not the title")

    for idx, ref in enumerate(as_list(data.get("references")), start=1):
        if not isinstance(ref, dict):
            fail(path, f"references[{idx}] must be a mapping")
            continue
        rid = ref.get("id")
        if not rid:
            fail(path, f"references[{idx}] missing id")
        if ref.get("relation") not in ALLOWED_REF_RELATION:
            fail(path, f"references[{idx}] invalid relation {ref.get('relation')}")

    if atype == "link_model":
        causal_order = as_list(data.get("causal_order"))
        if len(causal_order) < 3:
            fail(path, "link_model must have causal_order with at least 3 stages")
        if data.get("status") in {
            "candidate",
            "validated_seed",
            "validated_real_case",
            "generalized",
        }:
            if not data.get("debug_rules"):
                fail(path, "candidate+ link_model must include debug_rules")
            if not data.get("counterexamples"):
                warn(path, "link_model has no counterexamples")
        stage_model = as_list(data.get("stage_model"))
        if stage_model:
            for idx, stage in enumerate(stage_model, start=1):
                if not isinstance(stage, dict):
                    fail(path, f"stage_model[{idx}] must be a mapping")
                    continue
                if not stage.get("stage"):
                    fail(path, f"stage_model[{idx}] missing stage")
                if not any(
                    stage.get(k)
                    for k in ["measurement_points", "strong_indicators", "actions", "safe_actions"]
                ):
                    warn(path, f"stage_model[{idx}] has no measurement/indicator/action detail")

    elif atype == "signature":
        if not data.get("top_actions"):
            fail(path, "signature must have non-empty top_actions")
        min_match_count = data.get("min_match_count")
        if not min_match_count:
            fail(path, "signature must define min_match_count")
        elif not isinstance(min_match_count, int) or min_match_count < 1:
            fail(path, "min_match_count must be positive integer")
        if len(as_list(data.get("top_actions"))) < 2:
            warn(path, "signature has fewer than 2 top_actions")

    elif atype == "case_record":
        if not any(k in data for k in ["root_cause", "final_root_cause"]):
            fail(path, "case_record should include root_cause/final_root_cause")
        if data.get("source", {}).get("type") != "real_case" and data.get("status") in {
            "validated_real_case",
            "generalized",
        }:
            fail(path, "validated_real_case/generalized case_record must use source.type real_case")
        if not data.get("misleading_paths"):
            warn(path, "case_record has no misleading_paths")

    elif atype == "pattern_bundle":
        patterns = as_list(data.get("patterns") or data.get("pitfall_patterns"))
        if len(patterns) < 2:
            fail(path, "pattern_bundle must include at least 2 patterns/pitfall_patterns")
        for idx, pattern in enumerate(patterns, start=1):
            if not isinstance(pattern, dict):
                fail(path, f"pattern_bundle pattern[{idx}] must be a mapping")
                continue
            if not pattern.get("symptom"):
                fail(path, f"pattern_bundle pattern[{idx}] missing symptom")
            if not any(pattern.get(k) for k in ["first_checks", "actions", "diagnostic_checks"]):
                fail(
                    path,
                    f"pattern_bundle pattern[{idx}] missing first_checks/actions/diagnostic_checks",
                )
        if data.get("source", {}).get("type") == "real_case":
            fail(
                path,
                "pattern_bundle should not use source.type real_case; promote confirmed learning into case_record",
            )

    elif atype == "debug_principle":
        if not data.get("principle"):
            fail(path, "debug_principle must include principle")
        if not data.get("diagnostic_rule"):
            fail(path, "debug_principle must include diagnostic_rule")
        if not data.get("anti_patterns"):
            warn(path, "debug_principle has no anti_patterns")

# reference integrity after collecting ids
for path in asset_paths:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    for ref in as_list(data.get("references")):
        if isinstance(ref, dict):
            rid = ref.get("id")
            if rid and rid not in ids:
                fail(path, f"broken reference {rid}")

if errors:
    print("ASSET LINT FAILED")
    for e in errors:
        print("-", e)
    if warnings:
        print("WARNINGS")
        for w in warnings:
            print("-", w)
    sys.exit(1)

print(f"ASSET LINT PASSED: {len(ids)} assets")
if warnings:
    print("WARNINGS")
    for w in warnings:
        print("-", w)
