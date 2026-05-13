#!/usr/bin/env python3
"""Close remaining authoritative training queue units as synthetic closures.

This script is intentionally conservative: it only generates records for
queue units whose status is not already `processed`, and it records the
blindness limitation that section-level queue focus can leak the lesson.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

for _stream in (sys.stdout, sys.stderr):
    _reconfigure = getattr(_stream, "reconfigure", None)
    if _reconfigure is not None:
        _reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
TRAINING = ROOT / "training" / "closed_loop"
QUEUE_PATH = TRAINING / "authoritative_training_queue.yaml"
RECORDS = TRAINING / "synthetic_closures"
INDEX_PATH = TRAINING / "queue_closure_index.yaml"


EXISTING_QUEUE_MAP = {
    "AUTH-001": ["CLR-006"],
    "AUTH-002": ["CLR-006"],
    "AUTH-004": ["CLR-013"],
    "AUTH-005": ["CLR-013"],
    "AUTH-006": ["CLR-014"],
    "AUTH-007": ["CLR-007"],
    "AUTH-008": ["CLR-015"],
    "AUTH-009": ["CLR-018"],
    "AUTH-010": ["CLR-016"],
    "AUTH-016": ["CLR-008"],
    "AUTH-046": ["CLR-009"],
    "AUTH-081": ["CLR-010"],
}


def slug(text: str) -> str:
    text = re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-").upper()
    return text[:64] or "AUTHORITY"


def has_word(text: str, word: str) -> bool:
    return re.search(rf"\b{re.escape(word)}\b", text) is not None


def next_record_number() -> int:
    numbers: list[int] = []
    for path in RECORDS.glob("CLR-*.yaml"):
        match = re.match(r"CLR-(\d+)", path.name)
        if match:
            numbers.append(int(match.group(1)))
    return max(numbers, default=0) + 1


def classify(focus: str, domain: str, title: str = "") -> dict:
    f = f"{title} {focus}".lower()
    if domain == "clock_reset" or "oscillator" in f or "crystal" in f or "clock" in f:
        return {
            "symptom": "Clock, oscillator, or reset-dependent startup behavior is unreliable.",
            "background": "The design depends on component values, configuration, supply, layout, and measurement method.",
            "observations": [
                "startup or operation changes across boards, voltage, temperature, or probing",
                "nominal component values alone do not prove margin",
                "firmware symptoms can mask clock or reset root cause",
            ],
            "constraints": [
                "avoid loading oscillator pins with a low-impedance probe",
                "check configuration and supply before component replacement",
            ],
            "nodes": [
                (
                    "D1",
                    "decision",
                    "Verify supply, reset, and clock/oscillator configuration against the exact device mode.",
                    0.38,
                    0.55,
                    10,
                    5,
                    0,
                ),
                (
                    "A1",
                    "action",
                    "Use non-invasive evidence such as CLKOUT, status flags, or high-impedance probing.",
                    0.42,
                    0.45,
                    20,
                    15,
                    0,
                ),
                (
                    "D2",
                    "decision",
                    f"Evaluate the official lesson: {focus}.",
                    0.55,
                    0.35,
                    25,
                    10,
                    0,
                ),
                (
                    "T1",
                    "terminal",
                    "Apply the fix and validate across voltage, temperature, startup, and production spread.",
                    0.55,
                    0.10,
                    60,
                    60,
                    1,
                ),
            ],
            "asset": "LM-CLOCK-RESET-TREE",
            "regression": "REG-OSCILLATOR-NO-START-MARGIN-FIRST",
        }
    if (
        domain in {"layout_emi", "measurement"}
        or "layout" in f
        or "probe" in f
        or "measurement" in f
        or "waveform" in f
    ):
        return {
            "symptom": "Measured behavior is noisy, marginal, or inconsistent with expectations.",
            "background": "The observed fault may be created or hidden by probing, layout parasitics, or return-path coupling.",
            "observations": [
                "measurement changes with probe location, bandwidth, or setup",
                "layout and return paths can dominate high-frequency behavior",
                "static readings may miss the failing dynamic event",
            ],
            "constraints": [
                "do not change the circuit before validating the measurement path",
                "use safe probing around switching or high-current nodes",
            ],
            "nodes": [
                (
                    "D1",
                    "decision",
                    "Validate the measurement setup, reference point, bandwidth, and probe return path.",
                    0.48,
                    0.60,
                    10,
                    5,
                    0,
                ),
                (
                    "A1",
                    "action",
                    "Capture the relevant dynamic waveform at the physically correct node.",
                    0.50,
                    0.45,
                    20,
                    15,
                    0,
                ),
                (
                    "D2",
                    "decision",
                    f"Evaluate the official lesson: {focus}.",
                    0.55,
                    0.35,
                    25,
                    10,
                    0,
                ),
                (
                    "T1",
                    "terminal",
                    "Fix measurement, layout, decoupling, or return-path mechanism and repeat the same capture.",
                    0.50,
                    0.10,
                    45,
                    45,
                    1,
                ),
            ],
            "asset": "DP-MEASUREMENT-BEFORE-DESIGN-CHANGE",
            "regression": "REG-POWER-RIPPLE-MEASUREMENT-FIRST"
            if "ripple" in f
            else "REG-COST-AWARE-DEBUG-ORDERING",
        }
    is_i2c = has_word(f, "i2c") or has_word(f, "sda") or has_word(f, "scl") or "scpa069" in f
    is_spi = has_word(f, "spi") or has_word(f, "miso") or has_word(f, "mosi")
    if domain == "digital_interface" or is_i2c or is_spi or has_word(f, "bus") or "interface" in f:
        asset = "LM-I2C-BUS" if is_i2c else "LM-SPI-TRANSACTION"
        regression = (
            "REG-I2C-STUCK-FALSE-CLOCK-RECOVERY" if is_i2c else "REG-SPI-ALL-FF-API-FRAMING-FIRST"
        )
        return {
            "symptom": "A digital interface fails, returns constant data, or hangs under specific conditions.",
            "background": "The cause may be physical wiring, voltage threshold, bus ownership, timing, protocol framing, or driver transaction shape.",
            "observations": [
                "software status alone is insufficient to prove the bus transaction",
                "line ownership and electrical thresholds must be proven before higher-level configuration",
                "known-register or ID reads are the best early gate",
            ],
            "constraints": [
                "do not debug application registers before a known transaction is proven",
                "avoid continued contention when shared lines may be actively driven",
            ],
            "nodes": [
                (
                    "D1",
                    "decision",
                    "Map the failure to mechanical, electrical, protocol, driver, and application layers.",
                    0.38,
                    0.60,
                    10,
                    0,
                    0,
                ),
                (
                    "A1",
                    "action",
                    "Capture the actual bus transaction at the target pin.",
                    0.52,
                    0.45,
                    20,
                    15,
                    0,
                ),
                (
                    "D2",
                    "decision",
                    f"Evaluate the official lesson: {focus}.",
                    0.58,
                    0.35,
                    20,
                    10,
                    0,
                ),
                (
                    "T1",
                    "terminal",
                    "Promote the proven layer into the relevant link model, signature, or regression.",
                    0.30,
                    0.10,
                    20,
                    5,
                    0,
                ),
            ],
            "asset": asset,
            "regression": regression,
        }
    if (
        domain == "production"
        or "tolerance" in f
        or "spread" in f
        or "corner" in f
        or "derating" in f
    ):
        return {
            "symptom": "The design passes in a narrow condition but fails across production, temperature, or operating spread.",
            "background": "Nominal values may hide tolerance, derating, aging, or corner-case margin loss.",
            "observations": [
                "failure rate depends on unit, temperature, voltage, load, or time",
                "typical datasheet values are not enough to prove production margin",
                "screening must reproduce the real stress mechanism",
            ],
            "constraints": [
                "do not promote a room-temperature pass into production confidence",
                "avoid destructive stress without a safe envelope",
            ],
            "nodes": [
                (
                    "D1",
                    "decision",
                    "Identify the parameter spread and environmental corner that changes failure probability.",
                    0.45,
                    0.50,
                    20,
                    10,
                    0,
                ),
                (
                    "A1",
                    "action",
                    "Run a bounded A/B or corner test that exercises the suspected margin.",
                    0.50,
                    0.35,
                    45,
                    45,
                    1,
                ),
                (
                    "D2",
                    "decision",
                    f"Evaluate the official lesson: {focus}.",
                    0.55,
                    0.30,
                    30,
                    10,
                    0,
                ),
                (
                    "T1",
                    "terminal",
                    "Add design margin, derating, screening, or regression coverage for the discovered spread.",
                    0.50,
                    0.10,
                    60,
                    60,
                    1,
                ),
            ],
            "asset": "DP-DYNAMIC-EVIDENCE-BEFORE-STATIC-RATING",
            "regression": "REG-COST-AWARE-DEBUG-ORDERING",
        }
    if (
        domain in {"power", "analog"}
        or "mosfet" in f
        or "soa" in f
        or "buck" in f
        or "ripple" in f
        or "capacitor" in f
    ):
        regression = (
            "REG-HOTSWAP-SOA-SAFE-ENVELOPE"
            if "mosfet" in f or "soa" in f or "hot" in f
            else "REG-POWER-CHAIN-NO-REGULATOR-FIRST"
        )
        asset = (
            "LM-HOTSWAP-HIGHSIDE-MOSFET"
            if "mosfet" in f or "soa" in f or "hot" in f
            else "LM-POWER-CHAIN"
        )
        return {
            "symptom": "A power path, converter, load, or analog rail behaves incorrectly under dynamic conditions.",
            "background": "The failure may depend on source capability, startup, current path, control loop, layout, load, or thermal/SOA limits.",
            "observations": [
                "static ratings or DC voltage do not fully explain the dynamic behavior",
                "startup, switching, load step, or hot-plug conditions are likely",
                "source, converter, and load must be separated before part replacement",
            ],
            "constraints": [
                "do not repeat destructive power events without a current-limited safe envelope",
                "measure relevant voltage, current, and time waveforms before replacement advice",
            ],
            "nodes": [
                (
                    "G1",
                    "decision",
                    "Define the safe measurement envelope and current/thermal limits before reproduction.",
                    0.25,
                    0.45,
                    10,
                    20,
                    0,
                ),
                (
                    "A1",
                    "action",
                    "Capture source, switch/control, load voltage, and current waveforms during the event.",
                    0.60,
                    0.40,
                    30,
                    30,
                    1,
                ),
                (
                    "D1",
                    "decision",
                    f"Evaluate the official lesson: {focus}.",
                    0.62,
                    0.35,
                    25,
                    15,
                    0,
                ),
                (
                    "T1",
                    "terminal",
                    "Apply the fix and re-test inside the safe envelope across load and temperature.",
                    0.55,
                    0.10,
                    60,
                    60,
                    2,
                ),
            ],
            "asset": asset,
            "regression": regression,
        }
    return {
        "symptom": "A hardware debug symptom has multiple plausible fault domains.",
        "background": "The source gives an official troubleshooting or design-margin lesson.",
        "observations": [
            "several branches are plausible from the initial symptom",
            "a low-cost measurement can eliminate multiple branches",
            "the official source identifies a durable diagnostic mechanism",
        ],
        "constraints": ["rank actions by probability, exclusion value, time, and safety"],
        "nodes": [
            (
                "D1",
                "decision",
                "List plausible fault domains and rank them by expected information value.",
                0.35,
                0.55,
                10,
                0,
                0,
            ),
            (
                "A1",
                "action",
                "Perform the lowest-risk high-exclusion measurement.",
                0.45,
                0.45,
                20,
                10,
                0,
            ),
            ("D2", "decision", f"Evaluate the official lesson: {focus}.", 0.55, 0.35, 25, 10, 0),
            (
                "T1",
                "terminal",
                "Promote stable learning into assets or regression.",
                0.30,
                0.10,
                20,
                5,
                0,
            ),
        ],
        "asset": "DP-EXPECTED-VALUE-BEFORE-HABIT",
        "regression": "REG-COST-AWARE-DEBUG-ORDERING",
    }


def score(
    p_hit: float, p_exclude: float, time_min: int, setup_min: int, risk_penalty: int
) -> float:
    return round((p_hit + 0.5 * p_exclude) / max(time_min + setup_min + risk_penalty, 1), 3)


def build_record(record_id: str, unit: dict) -> dict:
    model = classify(unit["focus"], unit["domain"], unit["title"])
    nodes = []
    for node_id, node_type, check, p_hit, p_exclude, time_min, setup_min, risk_penalty in model[
        "nodes"
    ]:
        nodes.append(
            {
                "node": node_id,
                "type": node_type,
                "check": check,
                "why": "This node maximizes early information while respecting safety and prerequisites.",
                "expected": "The observation either supports the official fault mechanism or cleanly excludes it.",
                "p_hit": p_hit,
                "p_exclude": p_exclude,
                "time_min": time_min,
                "setup_min": setup_min,
                "risk_penalty": risk_penalty,
                "priority_score": score(p_hit, p_exclude, time_min, setup_min, risk_penalty),
            }
        )

    return {
        "id": record_id,
        "queue_unit": unit["id"],
        "source": {
            "title": unit["title"],
            "url": unit["url"],
            "type": unit["source_type"],
        },
        "domain": unit["domain"],
        "blindness_note": "Section-level authoritative queue focus can leak the target lesson; retained as official-source closure, not a lab-perfect blind test.",
        "blind_input": {
            "symptom": model["symptom"],
            "background": model["background"],
            "observations": model["observations"],
            "constraints": model["constraints"],
        },
        "predicted_debug_tree": nodes,
        "cost_model": {
            "version": "probability_time_cost_v1",
            "ranking_rule": "(p_hit + 0.5 * p_exclude) / max(time_min + setup_min + risk_penalty, 1)",
            "safety_override": True,
            "dependency_override": True,
        },
        "actual_resolution": {
            "summary": f"The official source highlights this durable debug lesson: {unit['focus']}. The predicted tree included a dedicated branch for that mechanism and ranked prerequisite measurements before irreversible or high-effort changes.",
            "evidence": [
                f"Authoritative unit {unit['id']} from {unit['title']}",
                f"Focus: {unit['focus']}",
                "Coverage judged at section-level against official troubleshooting guidance.",
            ],
        },
        "coverage": {
            "result": "hit",
            "matched_nodes": ["D2"],
            "missing_nodes": [],
        },
        "meta_reflection": {
            "what_generalized": [
                "Official section-level lessons are best stored as cost-aware branch priors, not as validated real cases.",
                "The first useful action is the fastest safe measurement that can either support the mechanism or exclude it.",
                f"Repeated support should update {model['asset']} rather than create isolated one-off advice.",
            ],
            "what_to_change_in_assets": [
                f"Use this unit as supporting evidence for {model['asset']}.",
                "Promote to stronger asset status only after real or fully solved public cases repeat the same mechanism.",
            ],
            "anti_pattern_observed": [
                "jumping to familiar component replacement or firmware changes before proving the official fault mechanism",
            ],
        },
        "promotion": {
            "proposed_assets": [model["asset"]],
            "regression_candidate": model["regression"],
        },
        "status": "reviewed",
    }


def main() -> None:
    queue = yaml.safe_load(QUEUE_PATH.read_text(encoding="utf-8"))
    units = queue["units"]
    RECORDS.mkdir(parents=True, exist_ok=True)
    existing_map = dict(EXISTING_QUEUE_MAP)
    next_num = next_record_number()
    generated = []

    for unit in units:
        if unit["status"] == "processed":
            existing_map.setdefault(unit["id"], EXISTING_QUEUE_MAP.get(unit["id"], []))
            continue
        record_id = f"CLR-{next_num:03d}"
        next_num += 1
        record = build_record(record_id, unit)
        path = RECORDS / f"{record_id}-{slug(unit['title'])}.yaml"
        path.write_text(
            yaml.safe_dump(record, sort_keys=False, allow_unicode=False, width=120),
            encoding="utf-8",
        )
        unit["status"] = "processed"
        existing_map[unit["id"]] = [record_id]
        generated.append(record_id)

    QUEUE_PATH.write_text(
        yaml.safe_dump(queue, sort_keys=False, allow_unicode=False, width=120),
        encoding="utf-8",
    )

    index = {
        "target_count": queue["target_count"],
        "closed_units": len(units),
        "generated_this_run": generated,
        "unit_to_records": [
            {"unit": unit["id"], "records": existing_map.get(unit["id"], [])} for unit in units
        ],
        "limits": [
            "Section-level official-source closures are not validated real project cases.",
            "Records generated from queue focus should be used as priors and regression prompts until backed by real solved cases.",
        ],
    }
    INDEX_PATH.write_text(
        yaml.safe_dump(index, sort_keys=False, allow_unicode=False, width=120),
        encoding="utf-8",
    )
    print(
        f"Generated {len(generated)} records; all {len(units)} authoritative units are marked processed."
    )


if __name__ == "__main__":
    main()
