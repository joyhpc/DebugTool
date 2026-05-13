#!/usr/bin/env python3
"""Lint the 1000-unit training program metadata and source queues."""

import sys
from pathlib import Path
from typing import Any

import yaml

for _stream in (sys.stdout, sys.stderr):
    _reconfigure = getattr(_stream, "reconfigure", None)
    if _reconfigure is not None:
        _reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "training" / "dataset_1000"
RECORDS = ROOT / "training" / "closed_loop" / "records"
SYNTHETIC_CLOSURES = ROOT / "training" / "closed_loop" / "synthetic_closures"
VALID_TIERS = {"T0", "T1", "T2", "T3", "T4", "T5"}
VALID_QUEUE_STATUS = {
    "queued_blind",
    "in_review",
    "reviewed",
    "reviewed_existing",
    "promoted",
    "blocked",
}
VALID_SOURCE_TYPES = {
    "public_solved_case",
    "vendor_forum_fae_resolved",
    "real_project_case",
    "official_source_prior",
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


def fail(path: Path, msg: str) -> None:
    errors.append(f"{path}: {msg}")


def warn(path: Path, msg: str) -> None:
    warnings.append(f"{path}: {msg}")


def as_list(value: object) -> list[Any]:
    return value if isinstance(value, list) else []


def collect_record_ids() -> set[str]:
    record_ids: set[str] = set()
    for record_dir in [RECORDS, SYNTHETIC_CLOSURES]:
        for path in record_dir.glob("CLR-*.yaml"):
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            if data.get("id"):
                record_ids.add(data["id"])
    return record_ids


target_path = DATASET / "target_mix.yaml"
status_path = DATASET / "status.yaml"
public_queue_path = DATASET / "public_solved_case_queue.yaml"
public_index_path = DATASET / "public_case_closure_index.yaml"
specialized_queues = [
    (
        DATASET / "intel_altera_fpga_queue.yaml",
        DATASET / "intel_altera_fpga_closure_index.yaml",
        "Intel/Altera FPGA",
    ),
    (
        DATASET / "mipi_debug_queue.yaml",
        DATASET / "mipi_debug_closure_index.yaml",
        "MIPI DSI/CSI",
    ),
]

for path in [target_path, status_path, public_queue_path]:
    if not path.exists():
        fail(path, "required dataset_1000 file is missing")

if target_path.exists():
    target = yaml.safe_load(target_path.read_text(encoding="utf-8")) or {}
    target_count = target.get("target_count")
    tiers = as_list(target.get("tiers"))
    if target_count != 1000:
        fail(target_path, "target_count must be 1000")
    tier_ids = set()
    tier_sum = 0
    for idx, tier in enumerate(tiers, start=1):
        if not isinstance(tier, dict):
            fail(target_path, f"tiers[{idx}] must be mapping")
            continue
        tid = tier.get("id")
        if tid not in VALID_TIERS:
            fail(target_path, f"tier {tid} must be one of {sorted(VALID_TIERS)}")
        if tid in tier_ids:
            fail(target_path, f"duplicate tier id {tid}")
        tier_ids.add(tid)
        tier_target = tier.get("target")
        if not isinstance(tier_target, int) or tier_target < 1:
            fail(target_path, f"tier {tid} target must be positive integer")
        else:
            tier_sum += tier_target
        for key in ["name", "description", "promotion_limit"]:
            if not tier.get(key):
                fail(target_path, f"tier {tid} missing {key}")
    if tier_sum != target_count:
        fail(target_path, f"tier targets sum to {tier_sum}, expected {target_count}")
    missing = VALID_TIERS - tier_ids
    if missing:
        fail(target_path, f"missing tier definitions: {', '.join(sorted(missing))}")

if status_path.exists():
    status = yaml.safe_load(status_path.read_text(encoding="utf-8")) or {}
    counts = status.get("current_counts") or {}
    if status.get("target_count") != 1000:
        fail(status_path, "target_count must be 1000")
    for key, value in counts.items():
        if not isinstance(value, int) or value < 0:
            fail(status_path, f"current_counts.{key} must be non-negative integer")
    closed_total = counts.get("closed_loop_records_total", 0)
    synthetic_total = counts.get("synthetic_closures_total", 0)
    official_closed = counts.get(
        "official_source_prior_synthetic_closures",
        counts.get("official_source_prior_closed", 0),
    )
    if (
        isinstance(closed_total, int)
        and isinstance(synthetic_total, int)
        and isinstance(official_closed, int)
        and closed_total + synthetic_total < official_closed
    ):
        fail(
            status_path,
            "closed_loop_records_total + synthetic_closures_total cannot be lower than official_source_prior_synthetic_closures",
        )
    if isinstance(closed_total, int) and closed_total == 0:
        warn(
            status_path,
            "closed_loop_records_total is zero; regression signal must come from blind/frozen eval",
        )
    real_project_reviewed = counts.get("real_project_reviewed_cases", 0)
    if isinstance(real_project_reviewed, int) and real_project_reviewed < 1:
        warn(status_path, "real_project_reviewed_cases is still below practical calibration needs")


def validate_source_queue(path: Path, label: str) -> None:
    queue = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    candidates = as_list(queue.get("candidates"))
    target_count = queue.get("target_count")
    if not isinstance(target_count, int) or target_count < 1:
        fail(path, f"{label} target_count must be positive integer")
    if queue.get("current_candidates") != len(candidates):
        fail(path, f"{label} current_candidates must match number of candidates")
    ids = set()
    for idx, cand in enumerate(candidates, start=1):
        if not isinstance(cand, dict):
            fail(path, f"{label} candidate[{idx}] must be mapping")
            continue
        cid = cand.get("id")
        if not cid:
            fail(path, f"{label} candidate[{idx}] missing id")
            continue
        if cid in ids:
            fail(path, f"{label} duplicate candidate id {cid}")
        ids.add(cid)
        for key in ["title", "url", "domain", "source_type", "expected_lesson", "status"]:
            if not cand.get(key):
                fail(path, f"{label} candidate {cid} missing {key}")
        if cand.get("domain") and cand.get("domain") not in VALID_DOMAINS:
            fail(path, f"{label} candidate {cid} invalid domain {cand.get('domain')}")
        if cand.get("source_type") and cand.get("source_type") not in VALID_SOURCE_TYPES:
            fail(path, f"{label} candidate {cid} invalid source_type {cand.get('source_type')}")
        if cand.get("status") and cand.get("status") not in VALID_QUEUE_STATUS:
            fail(path, f"{label} candidate {cid} invalid status {cand.get('status')}")


if public_queue_path.exists():
    validate_source_queue(public_queue_path, "public solved case")

if public_index_path.exists():
    index = yaml.safe_load(public_index_path.read_text(encoding="utf-8")) or {}
    record_ids = collect_record_ids()
    if index.get("target_count") != 300:
        fail(public_index_path, "target_count must be 300 for public solved cases")
    reviewed = index.get("reviewed_public_cases")
    if not isinstance(reviewed, int) or reviewed < 0:
        fail(public_index_path, "reviewed_public_cases must be non-negative integer")
    mapped_ids = set()
    for section in ["existing_records", "new_records"]:
        for idx, item in enumerate(as_list(index.get(section)), start=1):
            if not isinstance(item, dict):
                fail(public_index_path, f"{section}[{idx}] must be mapping")
                continue
            pid = item.get("public_case_id")
            records = as_list(item.get("records"))
            if not pid:
                fail(public_index_path, f"{section}[{idx}] missing public_case_id")
            if pid in mapped_ids:
                fail(public_index_path, f"duplicate public_case_id mapping {pid}")
            mapped_ids.add(pid)
            if not records:
                fail(public_index_path, f"{pid} has no records")
            for rid in records:
                if not str(rid).startswith("CLR-"):
                    fail(public_index_path, f"{pid} invalid record id {rid}")
                elif rid not in record_ids:
                    fail(public_index_path, f"{pid} maps to missing record {rid}")
    if reviewed != len(mapped_ids):
        fail(public_index_path, "reviewed_public_cases must match mapped public case count")

for queue_path, index_path, label in specialized_queues:
    if queue_path.exists():
        validate_source_queue(queue_path, label)
    if index_path.exists():
        index = yaml.safe_load(index_path.read_text(encoding="utf-8")) or {}
        record_ids = collect_record_ids()
        reviewed = index.get("reviewed_cases")
        mappings = as_list(index.get("case_to_records"))
        if not isinstance(reviewed, int) or reviewed < 0:
            fail(index_path, f"{label} reviewed_cases must be non-negative integer")
        seen = set()
        for idx, item in enumerate(mappings, start=1):
            if not isinstance(item, dict):
                fail(index_path, f"{label} case_to_records[{idx}] must be mapping")
                continue
            cid = item.get("case_id")
            records = as_list(item.get("records"))
            if not cid:
                fail(index_path, f"{label} case_to_records[{idx}] missing case_id")
            if cid in seen:
                fail(index_path, f"{label} duplicate case mapping {cid}")
            seen.add(cid)
            if not records:
                fail(index_path, f"{label} {cid} has no records")
            for rid in records:
                if rid not in record_ids:
                    fail(index_path, f"{label} {cid} maps to missing record {rid}")
        if reviewed != len(seen):
            fail(index_path, f"{label} reviewed_cases must match mapped case count")

if errors:
    print("DATASET 1000 LINT FAILED")
    for e in errors:
        print("-", e)
    if warnings:
        print("WARNINGS")
        for w in warnings:
            print("-", w)
    sys.exit(1)

print("DATASET 1000 LINT PASSED")
if warnings:
    print("WARNINGS")
    for w in warnings:
        print("-", w)
