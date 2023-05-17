# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`bma220`
================================================================================

BMA220 Bosch Circuitpython Driver library


* Author(s): Jose D. Montoya


"""

from micropython import const
from adafruit_bus_device import i2c_device
from adafruit_register.i2c_struct import ROUnaryStruct, UnaryStruct, Struct
from adafruit_register.i2c_bits import RWBits

try:
    from busio import I2C
    from typing import Tuple
except ImportError:
    pass


__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/jposada202020/CircuitPython_BMA220.git"


_REG_WHOAMI = const(0x00)
_ACC_RANGE = const(0x22)

# Acceleration range
ACC_RANGE_2 = const(0b00)
ACC_RANGE_4 = const(0b01)
ACC_RANGE_8 = const(0b10)
ACC_RANGE_16 = const(0b11)
acc_range_values = (ACC_RANGE_2, ACC_RANGE_4, ACC_RANGE_8, ACC_RANGE_16)
acc_range_factor = {0b00: 16, 0b01: 8, 0b10: 4, 0b11: 2}


class BMA220:
    """Driver for the BMA220 Sensor connected over I2C.

    :param ~busio.I2C i2c_bus: The I2C bus the BMA220 is connected to.
    :param int address: The I2C device address. Defaults to :const:`0x0A`

    :raises RuntimeError: if the sensor is not found

    **Quickstart: Importing and using the device**

    Here is an example of using the :class:`BMA220` class.
    First you will need to import the libraries to use the sensor

    .. code-block:: python

        import board
        import bma220

    Once this is done you can define your `board.I2C` object and define your sensor object

    .. code-block:: python

        i2c = board.I2C()  # uses board.SCL and board.SDA
        bma220 = bma220.BMA220(i2c)

    Now you have access to the attributes

    .. code-block:: python

        accx, accy, accz = bma.acceleration


    """

    _device_id = ROUnaryStruct(_REG_WHOAMI, "B")

    _acc_range = RWBits(2, _ACC_RANGE, 0)

    # Acceleration Data
    _acceleration = Struct(0x04, "BBB")

    def __init__(self, i2c_bus: I2C, address: int = 0x0A) -> None:
        self.i2c_device = i2c_device.I2CDevice(i2c_bus, address)

        if self._device_id != 0xDD:
            raise RuntimeError("Failed to find BMA220")

        self._acc_range_mem = self._acc_range

    @property
    def acc_range(self) -> str:
        """
        Sensor acc_range

        +---------------------------------+------------------+
        | Mode                            | Value            |
        +=================================+==================+
        | :py:const:`bma220.ACC_RANGE_2`  | :py:const:`0b00` |
        +---------------------------------+------------------+
        | :py:const:`bma220.ACC_RANGE_4`  | :py:const:`0b01` |
        +---------------------------------+------------------+
        | :py:const:`bma220.ACC_RANGE_8`  | :py:const:`0b10` |
        +---------------------------------+------------------+
        | :py:const:`bma220.ACC_RANGE_16` | :py:const:`0b11` |
        +---------------------------------+------------------+
        """
        values = (
            "ACC_RANGE_2",
            "ACC_RANGE_4",
            "ACC_RANGE_8",
            "ACC_RANGE_16",
        )
        return values[self._acc_range]

    @acc_range.setter
    def acc_range(self, value: int) -> None:
        if value not in acc_range_values:
            raise ValueError("Value must be a valid acc_range setting")
        self._acc_range = value
        self._acc_range_mem = value

    @property
    def acceleration(self):
        bufx, bufy, bufz = self._acceleration

        factor = acc_range_factor[self._acc_range_mem]

        return (
            self._twos_comp(bufx >> 2, 6) / factor,
            self._twos_comp(bufy >> 2, 6) / factor,
            self._twos_comp(bufz >> 2, 6) / factor,
        )

    @staticmethod
    def _twos_comp(val: int, bits: int) -> int:
        if val & (1 << (bits - 1)) != 0:
            return val - (1 << bits)
        return val
