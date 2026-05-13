# RTL8370 Switch Packet-Loss Field Action Plan

This is a synthetic dry-run instance of the generic templates:

- `forms/failure_matrix_template.md`
- `forms/same_window_evidence_batch_checklist.md`

Case-specific names stay in this file only.

## Artifact Navigation

- Start with `visual-architecture-brief.md` before assigning lab work.
- Use `latest-architecture-first.md` when a field result changes the boundary or mechanism ranking.
- Use `latest-input-cleaning.md` when new facts need provenance and synthetic dry-run limits.
- Return to `README.md` after adding, archiving, or renaming generated artifacts.

## 0. Executive Architecture Gate

Current top-level conclusion: this synthetic dry run must first prove where the packet disappears. The first subsystem is the packet evidence chain, not the named switch chip.

Use `visual-architecture-brief.md` as the first-page architecture map before assigning lab work.

| mode | visible symptom | first subsystem | P0 evidence batch | stop condition |
|---|---|---|---|---|
| Mode A | packet absent or unclear at ingress | traffic source / fixture / ingress path | ingress sequence capture and setup swap | Do not debug switch internals until ingress is proven valid. |
| Mode B | packet present at ingress but absent at egress | switch forwarding / port / config / environment | same-window counters, egress capture, config readback, environment | Do not change firmware or registers until counters/readback point there. |

## 1. Case Configuration

| generic_field | case_alias | allowed values / source | notes |
|---|---|---|---|
| sample_id | switch_unit_id | SW-001..SW-100 or lab inventory id | Required because the symptom is reported as 1/100 units. |
| subsystem_id | switch_chip_or_port_group | RTL8370, external PHY if present, port group, power/clock block | RTL8370 is an alias from the user input, not a datasheet-backed claim. |
| channel_id | port_or_traffic_direction | port id, ingress direction, egress direction, VLAN/queue/flow id | Add rows for actual observed ports/flows. |
| operation_id | uptime_traffic_profile_id | long-run soak, specific traffic pattern, reboot/recover test, cable/port swap | Must include uptime duration. |
| config_id | switch_config_profile_id | firmware build, register profile, EEPROM/strap profile, VLAN/QoS config | `unknown` is allowed but must be explicit. |
| test_window_id | packet_loss_window_id | timestamp, soak-run id, or packet-sequence window | Required for counter and packet-capture alignment. |
| failure_signature_id | packet_loss_signature | sequence gap, egress missing packet, CRC/link error, queue drop, unknown loss | Keep symptom signature separate from root cause. |
| evidence_batch_id | same_window_batch_id | RTL8370-SW-P0-BATCH-001, etc. | Links packet captures, counters, and environmental data. |

## 2. Failure Matrix Working Table

| matrix_id | switch_unit_id | switch_chip_or_port_group | port_or_traffic_direction | uptime_traffic_profile_id | switch_config_profile_id | packet_loss_window_id | test_count | pass_count | fail_count | failure_rate | packet_loss_signature | same_window_batch_id | confidence | notes |
|---|---|---|---|---|---|---|---:|---:|---:|---:|---|---|---|---|
| SW-MX-001 | affected unit | RTL8370 | unknown | long-run soak, duration unknown | unknown | unknown | 1 | 0 | 1 | 1.00 | packet loss after long uptime |  | low | Synthetic seed row; replace with measured run matrix. |
| SW-MX-002 | known-good comparison unit | RTL8370 | same as affected unit if possible | same long-run soak | same or measured config | unknown | 0 | 0 | 0 | 0.00 | none measured |  | low | Needs actual comparison data. |

Minimum before probability updates:

- `switch_unit_id`
- `port_or_traffic_direction`
- `uptime_traffic_profile_id`
- `switch_config_profile_id` or explicit `unknown`
- `packet_loss_window_id`
- `test_count`
- `fail_count`
- `packet_loss_signature`

## 3. P0 Same-Window Evidence Batch

All P0 evidence must share the same packet-loss window. Counters captured hours before or after the loss should be marked stale in the working notes and not used to lower a branch.

| evidence_id | boundary | capture | pass marker | fail marker | candidate_owner | status |
|---|---|---|---|---|---|---|
| SW-EV-P0-01 | traffic source / ingress | ingress packet sequence log and timestamp | packet enters expected ingress port with intact sequence | missing at ingress means source/test setup issue | lab/test owner | pending |
| SW-EV-P0-02 | switch port counters | per-port MIB, CRC, alignment, pause, underrun/overrun, drop/error counters | counters stable or explainable under load | drop/error/link counters rise with loss window | switch debug owner | pending |
| SW-EV-P0-03 | egress packet capture | egress capture with sequence id aligned to ingress | all ingress sequence ids appear at egress | packet present at ingress but absent at egress | lab/test owner | pending |
| SW-EV-P0-04 | power / clock / temperature | rail, clock or status proxy, board and chip temperature over uptime | no drift correlated with loss | thermal, rail, clock, reset, or brownout marker correlates with loss | hardware owner | pending |
| SW-EV-P0-05 | configuration readback | register/config snapshot before and during/after failure | fault unit matches expected profile and known-good unit | config bit, table, queue, VLAN, QoS, or port state differs | firmware/switch owner | pending |
| SW-EV-P0-06 | external link isolation | cable/port/peer swap or controlled comparison | failure stays with switch unit/port after external swap | failure follows cable, peer, tester, or traffic-generator port | lab/test owner | pending |

PM/project lead confirmation is required before treating candidate owners as formal assignments.

## 4. Decision Update Rules

- If packets are already missing at ingress capture, move to traffic source, tester, cable, or peer setup.
- If ingress is valid and egress is missing while switch drop/error counters rise, keep the boundary inside switch forwarding, queue, port MAC/PHY, or configuration state.
- If link/CRC/alignment errors rise, prioritize PHY/link/SI/cable/connector/port margin before switch forwarding logic.
- If temperature, rail, clock, reset, or brownout markers correlate with loss after uptime, prioritize board-level prerequisite drift.
- If configuration readback changes after long uptime or differs from known-good units, prioritize configuration retention, firmware task, strap/EEPROM, or control path.
- If all same-window evidence is clean but loss persists, keep `unknown / model gap` active and expand instrumentation before changing hardware.

## 5. Stop Conditions

- Stop calling RTL8370 the root cause until ingress/egress capture and same-window counters locate the first-fail boundary.
- Stop using the 1/100 distribution as proof of a board defect until unit, port, traffic, uptime, and config axes are logged.
- Stop changing firmware or register settings as a fix until config readback or counter evidence points there.
- Stop excluding the test setup until the loss is shown not to follow cable, peer, traffic-generator port, or tester configuration.
