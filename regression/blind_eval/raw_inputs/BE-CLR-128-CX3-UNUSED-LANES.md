# Blind Input: CX3 MIPI CSI No Frame

## Symptom

Infineon CX3 MIPI CSI design has no video or no frame detection.

## Background

The design uses fewer MIPI data lanes than the CX3 supports. Debug prints and
an error thread can be enabled.

## Observations

- Valid CSI framing may not be detected.
- One or more unused MIPI data lanes may be left floating.

## Constraints

- Do not assume firmware can compensate for a strict hardware lane requirement.
