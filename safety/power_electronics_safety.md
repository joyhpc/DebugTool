# Power Electronics Safety

## Hot-swap / MOSFET / Inrush

1. Use current-limited source before reproduction.
2. Do not repeatedly perform full-power hot-plug tests.
3. Capture VGS, VDS, and current during turn-on.
4. Check Miller plateau and linear-region dwell time.
5. Compare pulse stress against MOSFET SOA, not only RDS(on).
6. Estimate load capacitance energy and inrush profile.
7. Check gate resistor, driver strength, charge pump/bootstrap, and soft-start.
8. Start with reduced load capacitance/current where possible.
9. Check thermal path and estimate Tj, not only case temperature.
10. Consider avalanche, reverse polarity, and body diode stress.

## High Voltage / Large Energy

11. Verify discharge of bulk capacitors before handling.
12. Use probes rated for voltage and common-mode conditions.
13. Avoid unsafe earth-referenced scope probing.
14. Use differential or isolated probing when required.
15. Keep insulation practices for high-voltage work where applicable.

## Battery / Motor

16. Check BMS state before bypassing protection.
17. Do not short or directly stress lithium packs.
18. Account for regenerative energy in motor systems.
19. Clamp or absorb bus energy during braking tests.
20. Control mechanical motion before electrical perturbation.

## Measurement Pitfalls

21. Minimize loop area in high-current switching measurements.
22. Do not mistake probe-induced ringing for circuit behavior.
23. Check current probe degauss/offset.
24. Check thermal camera emissivity.
25. Document safe setup before perturb/reproduce actions.
