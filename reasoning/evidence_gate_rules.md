# Evidence Gate Rules

- SPI decode branch requires raw SPI waveform.
- I2C address branch requires idle-high bus and visible address byte.
- PCIe LTSSM branch requires power, REFCLK, and PERST# valid.
- DB pool branch requires timing evidence pointing to DB/pool.
- Hot-swap SOA branch requires VGS/VDS/ID or equivalent stress evidence.
