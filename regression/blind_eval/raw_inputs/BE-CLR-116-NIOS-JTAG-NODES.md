# Blind Input: FPGA Visible But Nios Debug Missing

## Symptom

The FPGA can be seen over JTAG, but Nios debug or JTAG UART access is missing
or ambiguous.

## Background

A Platform Designer/Nios system may or may not contain the debug module, JTAG
UART, and SLD hub nodes in the loaded SOF.

## Observations

- External device ID detection can succeed while internal debug services are absent.
- Software tools may report target connection failures after SOF programming.

## Constraints

- Do not conflate FPGA IDCODE detection with presence of Nios debug nodes.
- Separate external JTAG chain health from internal design-content visibility.
