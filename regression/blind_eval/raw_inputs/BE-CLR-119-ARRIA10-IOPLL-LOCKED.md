# Blind Input: Arria 10 IOPLL Locked Output

## Symptom

Arria 10 IOPLL locked output is low, delayed, or misunderstood during bring-up.

## Background

The reference clock, reset, and PLL output may be probed while the design is
being released from reset.

## Observations

- PLL lock is sometimes treated as immediate once reset is released.
- Reference-clock stability and digital filtering may not be accounted for.

## Constraints

- Do not release downstream logic solely from a guessed PLL state.
- Explain what evidence is needed before using locked as a control signal.
