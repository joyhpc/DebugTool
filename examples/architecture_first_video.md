# Example — Architecture-First Video Link

Input:

```text
HDMI receiver → FPGA → LVDS panel. Intermittent black screen after source switching, temperature-related.
```

Expected:

- Not Fast Path.
- Use LM-VIDEO-LINK.
- Include reproduction/isolation:
  - temperature sweep
  - source switching repeatability
  - receiver lock status
  - FPGA clock/reset/frame status
  - LVDS/panel init/backlight
