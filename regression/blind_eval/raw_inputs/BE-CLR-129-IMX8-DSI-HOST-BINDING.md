# Blind Input: i.MX8 DSI No Waveform

## Symptom

i.MX8 MIPI-DSI display has no image and no MIPI waveform can be measured, while
another Android target/profile displays normally.

## Background

The path is MIPI-DSI to serializer/deserializer to LVDS. Software build/profile
differs between working and failing cases.

## Observations

- No MIPI waveform is visible in the failing profile.
- A different lunch target produces display and measurable waveform.

## Constraints

- Do not conclude board routing failure until the DSI host binding/enabling path
  is proven.
