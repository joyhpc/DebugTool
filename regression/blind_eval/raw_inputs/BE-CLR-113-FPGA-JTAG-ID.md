# Blind Input: FPGA Device ID Not Recognized

## Symptom

Quartus Programmer fails to recognize an Intel/Altera FPGA device ID.

## Background

The board is in a configuration or JTAG bring-up state. The user may be tempted
to change programming files, selected device entries, or project settings.

## Observations

- Device ID cannot be read reliably or at all.
- Configuration pins and dedicated JTAG pins may share the failure boundary.

## Constraints

- Capture signals at the FPGA end; connector-only measurements can hide board
  path faults.
- Do not start by changing the programming file or bitstream.
