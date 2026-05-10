# Blind Input: MIPI D-PHY Does Not Enter HS

## Symptom

MIPI D-PHY link does not initialize or does not enter HS clock/data transfer.

## Background

The PHY exposes PPI stopstate, init_done, lock signals, CL/DL status registers,
and HS/LP error indicators.

## Observations

- LP11 and stopstate are prerequisite states before HS traffic.
- HS clock transfer and HS data transfer are separate steps.

## Constraints

- Do not debug packet layer before lane initialization and HS clock are proven.
