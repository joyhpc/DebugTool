# Blind Input: Jetson CSI Camera Timeout

## Symptom

Jetson CSI camera sensor times out or produces no frames during bring-up.

## Background

The driver has device-tree mode settings, sensor power_on sequencing, I2C
access, and MIPI CSI configuration fields.

## Observations

- Sensor timeout can occur even when the driver loads.
- I2C errors and wrong mode-specific settings have different first checks.

## Constraints

- Do not rewrite image processing or userspace capture before kernel mode
  settings and I2C/power evidence are checked.
