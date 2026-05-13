#!/usr/bin/env python3
"""Lint closed-loop debug training records."""

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
TRAINING = ROOT / "training" / "closed_loop"
VALID_RESULTS = {"hit", "near_hit", "miss", "blocked"}
VALID_STATUS = {"draft", "reviewed", "promoted"}
VALID_QUEUE_STATUS = {"queued_blind", "in_review", "processed", "reference_only"}
VALID_SOURCE_TYPES = {
    "vendor_app_note",
    "vendor_design_guide",
    "vendor_training",
    "datasheet",
    "official_checklist",
}
VALID_DOMAINS = {
    "power",
    "measurement",
    "digital_interface",
    "clock_reset",
    "analog",
    "production",
    "layout_emi",
    "other",
}

errors: list[str] = []
warnings: list[str] = []


def as_list(value: object) -> list[Any]:
    return value if isinstance(value, list) else []


def fail(path: Path, msg: str) -> None:
    errors.append(f"{path}: {msg}")


def warn(path: Path, msg: str) -> None:
    warnings.append(f"{path}: {msg}")


queue_path = TRAINING / "candidate_sources.yaml"
if not queue_path.exists():
    fail(queue_path, "missing candidate source queue")
else:
    queue = yaml.safe_load(queue_path.read_text(encoding="utf-8")) or {}
    candidates = as_list(queue.get("candidates"))
    target_count = queue.get("target_count")
    if not isinstance(target_count, int) or target_count < 1:
        fail(queue_path, "target_count must be positive integer")
    if not candidates:
        fail(queue_path, "candidates must be non-empty")
    ids = set()
    for idx, cand in enumerate(candidates, start=1):
        cid = cand.get("id") if isinstance(cand, dict) else None
        if not cid:
            fail(queue_path, f"candidate[{idx}] missing id")
            continue
        if cid in ids:
            fail(queue_path, f"duplicate candidate id {cid}")
        ids.add(cid)
        for key in ["title", "url", "domain", "status"]:
            if not cand.get(key):
                fail(queue_path, f"candidate {cid} missing {key}")

auth_queue_path = TRAINING / "closed_loop" / "authoritative_training_queue.yaml"
if not auth_queue_path.exists():
    auth_queue_path = TRAINING / "authoritative_training_queue.yaml"

if not auth_queue_path.exists():
    fail(auth_queue_path, "missing authoritative training queue")
else:
    auth_queue = yaml.safe_load(auth_queue_path.read_text(encoding="utf-8")) or {}
    units = as_list(auth_queue.get("units"))
    target_count = auth_queue.get("target_count")
    current_units = auth_queue.get("current_units")
    if not isinstance(target_count, int) or target_count < 1:
        fail(auth_queue_path, "target_count must be positive integer")
    if not isinstance(current_units, int) or current_units != len(units):
        fail(auth_queue_path, "current_units must match number of units")
    if isinstance(target_count, int) and len(units) < target_count:
        fail(auth_queue_path, "units must meet target_count")
    ids = set()
    for idx, unit in enumerate(units, start=1):
        if not isinstance(unit, dict):
            fail(auth_queue_path, f"unit[{idx}] must be mapping")
            continue
        uid = unit.get("id")
        if not uid:
            fail(auth_queue_path, f"unit[{idx}] missing id")
            continue
        if uid in ids:
            fail(auth_queue_path, f"duplicate unit id {uid}")
        ids.add(uid)
        for key in ["title", "url", "source_type", "domain", "focus", "status"]:
            if not unit.get(key):
                fail(auth_queue_path, f"unit {uid} missing {key}")
        if unit.get("source_type") and unit.get("source_type") not in VALID_SOURCE_TYPES:
            fail(auth_queue_path, f"unit {uid} invalid source_type {unit.get('source_type')}")
        if unit.get("domain") and unit.get("domain") not in VALID_DOMAINS:
            fail(auth_queue_path, f"unit {uid} invalid domain {unit.get('domain')}")
        if unit.get("status") and unit.get("status") not in VALID_QUEUE_STATUS:
            fail(auth_queue_path, f"unit {uid} invalid status {unit.get('status')}")

closure_index_path = TRAINING / "queue_closure_index.yaml"
closure_index = None
if closure_index_path.exists():
    closure_index = yaml.safe_load(closure_index_path.read_text(encoding="utf-8")) or {}

record_paths = sorted((TRAINING / "records").glob("*.yaml"))
if not record_paths:
    fail(TRAINING / "records", "no closed-loop records found")

record_ids: set[str] = set()

for path in record_paths:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    rid = data.get("id")
    if not rid:
        fail(path, "missing id")
    elif not str(rid).startswith("CLR-"):
        fail(path, "id should start with CLR-")
    else:
        if rid in record_ids:
            fail(path, f"duplicate record id {rid}")
        record_ids.add(rid)

    source = data.get("source") or {}
    if not source.get("url"):
        fail(path, "source.url is required")
    if not source.get("title"):
        fail(path, "source.title is required")

    blind = data.get("blind_input") or {}
    if not blind.get("symptom"):
        fail(path, "blind_input.symptom is required")
    if not as_list(blind.get("observations")):
        warn(path, "blind_input.observations is empty")

    tree = as_list(data.get("predicted_debug_tree"))
    if len(tree) < 3:
        fail(path, "predicted_debug_tree must include at least 3 nodes")

    cost_model = data.get("cost_model") or {}
    if data.get("status") in {"reviewed", "promoted"} and not cost_model:
        warn(path, "reviewed record has no cost_model; legacy record should be upgraded")
    if cost_model:
        if cost_model.get("version") != "probability_time_cost_v1":
            fail(path, "cost_model.version must be probability_time_cost_v1")
        for idx, node in enumerate(tree, start=1):
            if not isinstance(node, dict):
                fail(path, f"node[{idx}] cost fields require a mapping node")
                continue
            node_id = node.get("node", f"node[{idx}]")
            for key in [
                "p_hit",
                "p_exclude",
                "time_min",
                "setup_min",
                "risk_penalty",
                "priority_score",
            ]:
                if key not in node:
                    fail(path, f"{node_id} missing cost field {key}")
                    continue
                value = node.get(key)
                if key in {"p_hit", "p_exclude"}:
                    if not isinstance(value, (int, float)) or value < 0 or value > 1:
                        fail(path, f"{node_id}.{key} must be 0.0-1.0")
                elif key in {"time_min", "setup_min", "risk_penalty", "priority_score"} and (
                    not isinstance(value, (int, float)) or value < 0
                ):
                    fail(path, f"{node_id}.{key} must be non-negative")

    actual = data.get("actual_resolution") or {}
    if not actual.get("summary"):
        fail(path, "actual_resolution.summary is required")

    coverage = data.get("coverage") or {}
    if coverage.get("result") not in VALID_RESULTS:
        fail(path, f"coverage.result must be one of {sorted(VALID_RESULTS)}")

    reflection = data.get("meta_reflection") or {}
    if not as_list(reflection.get("what_generalized")):
        warn(path, "meta_reflection.what_generalized is empty")

    if data.get("status") not in VALID_STATUS:
        fail(path, f"status must be one of {sorted(VALID_STATUS)}")

if closure_index is not None:
    auth_queue = yaml.safe_load(auth_queue_path.read_text(encoding="utf-8")) or {}
    units = as_list(auth_queue.get("units"))
    unit_ids: list[str] = []
    for unit in units:
        if not isinstance(unit, dict):
            continue
        unit_id = unit.get("id")
        if isinstance(unit_id, str):
            unit_ids.append(unit_id)
    if closure_index.get("target_count") != auth_queue.get("target_count"):
        fail(closure_index_path, "target_count must match authoritative queue")
    if closure_index.get("closed_units") != len(unit_ids):
        fail(closure_index_path, "closed_units must match authoritative queue unit count")
    mappings = as_list(closure_index.get("unit_to_records"))
    mapped: dict[str, list[Any]] = {}
    for idx, item in enumerate(mappings, start=1):
        if not isinstance(item, dict):
            fail(closure_index_path, f"unit_to_records[{idx}] must be mapping")
            continue
        unit = item.get("unit")
        records = as_list(item.get("records"))
        if not isinstance(unit, str) or not unit:
            fail(closure_index_path, f"unit_to_records[{idx}] missing unit")
            continue
        if unit in mapped:
            fail(closure_index_path, f"duplicate closure mapping for {unit}")
        mapped[unit] = records
        if not records:
            fail(closure_index_path, f"{unit} has no mapped records")
        for rid in records:
            if rid not in record_ids:
                fail(closure_index_path, f"{unit} maps to missing record {rid}")
    missing_units = sorted(set(unit_ids) - set(mapped))
    if missing_units:
        fail(closure_index_path, f"missing closure mappings for {', '.join(missing_units)}")
    queued_units: list[str] = []
    for unit in units:
        if not isinstance(unit, dict) or unit.get("status") == "processed":
            continue
        unit_id = unit.get("id")
        if isinstance(unit_id, str):
            queued_units.append(unit_id)
    if queued_units:
        fail(
            closure_index_path,
            f"authoritative queue not fully processed: {', '.join(queued_units)}",
        )

if errors:
    print("CLOSED LOOP LINT FAILED")
    for e in errors:
        print("-", e)
    if warnings:
        print("WARNINGS")
        for w in warnings:
            print("-", w)
    sys.exit(1)

print(f"CLOSED LOOP LINT PASSED: {len(record_paths)} records")
if warnings:
    print("WARNINGS")
    for w in warnings:
        print("-", w)
