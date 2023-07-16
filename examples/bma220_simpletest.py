# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
import board
from bma220 import bma220

i2c = board.I2C()  # uses board.SCL and board.SDA
bma = bma220.BMA220(i2c)

while True:
    accx, accy, accz = bma.acceleration
    print(f"x:{accx:.2f}m/s², y:{accy:.2f}m/s², z:{accz:.2f}m/s²")
    time.sleep(0.1)
