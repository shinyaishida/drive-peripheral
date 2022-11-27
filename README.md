# drive-peripheral

BLE peripheral to drive remote control car

## Prerequisites

- Raspberry Pi (developed and tested with 3B)
  - [Raspberry Pi OS (Raspbian)](https://www.raspberrypi.com/software/)
  - [ServoBlaster](https://github.com/richardghirst/PiBits/tree/master/ServoBlaster)
  - Python (developed and tested with version 3.10.7)
  - [Poetry](https://python-poetry.org/)
- Remote control car
  - Compatible with [this model](https://tamiyashop.jp/shop/g/g58615/)
- Male/Female jumper wires
  - Three for ground, steering, and acceleration

## Install peripheral

Run the following commands on a Raspberri Pi device to install the drive peripheral.
```bash
% git clone https://github.com/shinyaishida/drive-peripheral.git
% cd drive-peripheral
% sudo env PATH=$PATH poetry install --no-root
```

If you are going to edit the peripheral source code on the device, run the following
command.
```bash
% poetry install --no-root
```

## Run peripheral

Create `.env` in the root directory and set UUIDs as environment variables.
```bash
# BLE service UUID
SERVICE_UUID=XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
# UUID of control characteristic
CONTROL_CHAR_UUID=XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
# UUID of driving characteristic
DRIVE_CHAR_UUID=XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
```

Peripheral must be run as root.
```bash
% sudo env PATH=$PATH poetry run python drive-peripheral/drive_peripheral.py
Starting drive peripheral
state changed to poweredOn
started advertising: success
```

Then, start the Steering Wheel application. A sample application is available
[here](https://github.com/shinyaishida/steering-wheel-ios12). If it is connected with
the peripheral, the console prints this line.
```bash
subscribed
```

Now the steering wheel can send signals to the peripheral.
```bash
received data 'bytearray(b'Forward')'
received data 'bytearray(b'Neutral')'
  ...
```

## Run tests

```bash
% poetry run pytest
```

## License

MIT

## Author

Shinya Ishida
