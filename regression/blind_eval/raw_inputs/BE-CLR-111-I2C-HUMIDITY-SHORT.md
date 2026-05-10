# Blind Input: Humid I2C SDA Stuck Low

## Symptom

Arduino-class board with several I2C modules freezes; SDA goes low and remains
stuck during writes.

## Background

Boards were installed in humid enclosures. Some sensors were powered from GPIOs
and multiple breakout modules share I2C.

## Observations

- Moisture deposits were seen inside enclosures.
- Some boards recovered after removing an RTC breakout and moving pull-ups to VCC.
- One accelerometer SCL pin appeared damaged.

## Constraints

- Do not treat this as pure protocol until contamination and damaged IO are isolated.
