# 1000-Unit Debug Training Program

Purpose: expand from 100 official-source priors to a 1000-unit training set without confusing queue volume with validated debug skill.

## Target Mix

The 1000 units must include multiple evidence classes:

- Official principles and app-note sections
- Public solved debug cases
- Vendor forum / FAE resolved cases
- Real project reviewed cases
- Counterexamples, near-hit, miss, and misleading-path records
- High-risk safety cases

## Closure Definition

A unit is closed only when it has:

- source provenance
- blind input
- predicted debug tree
- probability/time-cost fields
- actual resolution or official lesson reveal
- hit / near_hit / miss / blocked score
- meta-reflection
- promotion decision

## Quality Rule

Do not promote official-source section closures as `validated_real_case`. They are priors. Real project cases and fully solved public cases are the main calibration data.

## Current Direction

1. Keep official-source closures as T0 priors.
2. Add public solved debug cases as T1/T2 calibration records.
3. Route user-supplied project cases through `training/real_project_cases/`.
4. Convert near-hit/miss into counterexamples, signatures, link-model refinements, and regression tests.
5. Grow focused domain queues such as `intel_altera_fpga_queue.yaml` and `mipi_debug_queue.yaml` when a hardware family or interface needs repeated, evidence-grounded calibration.
