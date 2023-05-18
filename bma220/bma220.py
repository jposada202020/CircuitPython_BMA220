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
from adafruit_register.i2c_struct import ROUnaryStruct, Struct
from adafruit_register.i2c_bits import RWBits
from adafruit_register.i2c_bit import RWBit

try:
    from busio import I2C
    from typing import Tuple
except ImportError:
    pass


__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/jposada202020/CircuitPython_BMA220.git"


_REG_WHOAMI = const(0x00)
_FILTER_CONF = const(0x20)
_ACC_RANGE = const(0x22)
_SLEEP_CONF = const(0x0F)
_LATCH_CONF = const(0x1C)

# Acceleration range
ACC_RANGE_2 = const(0b00)
ACC_RANGE_4 = const(0b01)
ACC_RANGE_8 = const(0b10)
ACC_RANGE_16 = const(0b11)
acc_range_values = (ACC_RANGE_2, ACC_RANGE_4, ACC_RANGE_8, ACC_RANGE_16)
acc_range_factor = {0b00: 16, 0b01: 8, 0b10: 4, 0b11: 2}

SLEEP_DISABLED = const(0b0)
SLEEP_ENABLED = const(0b1)
sleep_enabled_values = (SLEEP_DISABLED, SLEEP_ENABLED)

# Sleep Duration
SLEEP_2MS = const(0b000)
SLEEP_10MS = const(0b001)
SLEEP_25MS = const(0b010)
SLEEP_50MS = const(0b011)
SLEEP_100MS = const(0b100)
SLEEP_500MS = const(0b101)
SLEEP_1S = const(0b110)
SLEEP_2S = const(0b111)
sleep_duration_values = (
    SLEEP_2MS,
    SLEEP_10MS,
    SLEEP_25MS,
    SLEEP_50MS,
    SLEEP_100MS,
    SLEEP_500MS,
    SLEEP_1S,
    SLEEP_2S,
)

# Axis Enabled Values
X_DISABLED = const(0b0)
X_ENABLED = const(0b1)
Y_DISABLED = const(0b0)
Y_ENABLED = const(0b1)
Z_DISABLED = const(0b0)
Z_ENABLED = const(0b1)
axis_enabled_values = (X_DISABLED, X_ENABLED)

# Filter Bandwidth
ACCEL_32HZ = const(0x05)
ACCEL_64HZ = const(0x04)
ACCEL_125HZ = const(0x03)
ACCEL_250HZ = const(0x02)
ACCEL_500HZ = const(0x01)
ACCEL_1000HZ = const(0x00)
filter_bandwidth_values = (
    ACCEL_32HZ,
    ACCEL_64HZ,
    ACCEL_125HZ,
    ACCEL_250HZ,
    ACCEL_500HZ,
    ACCEL_1000HZ,
)

UNLATCHED = const(0b000)
LATCH_FOR_025S = const(0b001)
LATCH_FOR_050S = const(0b010)
LATCH_FOR_1S = const(0b011)
LATCH_FOR_2S = const(0b100)
LATCH_FOR_4S = const(0b101)
LATCH_FOR_8S = const(0b110)
LATCHED = const(0b111)
latched_mode_values = (
    UNLATCHED,
    LATCH_FOR_025S,
    LATCH_FOR_050S,
    LATCH_FOR_1S,
    LATCH_FOR_2S,
    LATCH_FOR_4S,
    LATCH_FOR_8S,
    LATCHED,
)


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
    _filter_bandwidth = RWBits(4, _FILTER_CONF, 0)
    _latched_mode = RWBits(3, _LATCH_CONF, 4)

    # Acceleration Data
    _acceleration = Struct(0x04, "BBB")

    # Register (0x0F)
    # |----|sleep_en|sleep_dur(2)|sleep_dur(1)|sleep_dur(0)|en_x_channel|en_y_channel|en_z_channel|
    _z_enabled = RWBit(_SLEEP_CONF, 0)
    _y_enabled = RWBit(_SLEEP_CONF, 1)
    _x_enabled = RWBit(_SLEEP_CONF, 2)
    _sleep_duration = RWBits(3, _SLEEP_CONF, 3)
    _sleep_enabled = RWBit(_SLEEP_CONF, 6)

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
    def sleep_enabled(self) -> str:
        """
        Sensor sleep_enabled

        +-----------------------------------+-----------------+
        | Mode                              | Value           |
        +===================================+=================+
        | :py:const:`bma220.SLEEP_DISABLED` | :py:const:`0b0` |
        +-----------------------------------+-----------------+
        | :py:const:`bma220.SLEEP_ENABLED`  | :py:const:`0b1` |
        +-----------------------------------+-----------------+
        """
        values = ("SLEEP_DISABLED", "SLEEP_ENABLED")
        return values[self._sleep_enabled]

    @sleep_enabled.setter
    def sleep_enabled(self, value: int) -> None:
        if value not in sleep_enabled_values:
            raise ValueError("Value must be a valid sleep_enabled setting")
        self._sleep_enabled = value

    @property
    def sleep_duration(self) -> str:
        """
        Sensor sleep_duration

        +--------------------------------+-------------------+
        | Mode                           | Value             |
        +================================+===================+
        | :py:const:`bma220.SLEEP_2MS`   | :py:const:`0b000` |
        +--------------------------------+-------------------+
        | :py:const:`bma220.SLEEP_10MS`  | :py:const:`0b001` |
        +--------------------------------+-------------------+
        | :py:const:`bma220.SLEEP_25MS`  | :py:const:`0b010` |
        +--------------------------------+-------------------+
        | :py:const:`bma220.SLEEP_50MS`  | :py:const:`0b011` |
        +--------------------------------+-------------------+
        | :py:const:`bma220.SLEEP_100MS` | :py:const:`0b100` |
        +--------------------------------+-------------------+
        | :py:const:`bma220.SLEEP_500MS` | :py:const:`0b101` |
        +--------------------------------+-------------------+
        | :py:const:`bma220.SLEEP_1S`    | :py:const:`0b110` |
        +--------------------------------+-------------------+
        | :py:const:`bma220.SLEEP_2S`    | :py:const:`0b111` |
        +--------------------------------+-------------------+
        """
        values = (
            "SLEEP_2MS",
            "SLEEP_10MS",
            "SLEEP_25MS",
            "SLEEP_50MS",
            "SLEEP_100MS",
            "SLEEP_500MS",
            "SLEEP_1S",
            "SLEEP_2S",
        )
        return values[self._sleep_duration]

    @sleep_duration.setter
    def sleep_duration(self, value: int) -> None:
        if value not in sleep_duration_values:
            raise ValueError("Value must be a valid sleep_duration setting")
        self._sleep_duration = value

    @property
    def x_enabled(self) -> str:
        """
        Sensor x_enabled

        +-------------------------------+-----------------+
        | Mode                          | Value           |
        +===============================+=================+
        | :py:const:`bma220.X_DISABLED` | :py:const:`0b0` |
        +-------------------------------+-----------------+
        | :py:const:`bma220.X_ENABLED`  | :py:const:`0b1` |
        +-------------------------------+-----------------+
        """
        values = (
            "X_DISABLED",
            "X_ENABLED",
        )
        return values[self._x_enabled]

    @x_enabled.setter
    def x_enabled(self, value: int) -> None:
        if value not in axis_enabled_values:
            raise ValueError("Value must be a valid x_enabled setting")
        self._x_enabled = value

    @property
    def y_enabled(self) -> str:
        """
        Sensor y_enabled

        +-------------------------------+-----------------+
        | Mode                          | Value           |
        +===============================+=================+
        | :py:const:`bma220.Y_DISABLED` | :py:const:`0b0` |
        +-------------------------------+-----------------+
        | :py:const:`bma220.Y_ENABLED`  | :py:const:`0b1` |
        +-------------------------------+-----------------+
        """
        values = (
            "Y_DISABLED",
            "Y_ENABLED",
        )
        return values[self._y_enabled]

    @y_enabled.setter
    def y_enabled(self, value: int) -> None:
        if value not in axis_enabled_values:
            raise ValueError("Value must be a valid y_enabled setting")
        self._y_enabled = value

    @property
    def z_enabled(self) -> str:
        """
        Sensor z_enabled

        +-------------------------------+-----------------+
        | Mode                          | Value           |
        +===============================+=================+
        | :py:const:`bma220.Z_DISABLED` | :py:const:`0b0` |
        +-------------------------------+-----------------+
        | :py:const:`bma220.Z_ENABLED`  | :py:const:`0b1` |
        +-------------------------------+-----------------+
        """
        values = (
            "Z_DISABLED",
            "Z_ENABLED",
        )
        return values[self._z_enabled]

    @z_enabled.setter
    def z_enabled(self, value: int) -> None:
        if value not in axis_enabled_values:
            raise ValueError("Value must be a valid z_enabled setting")
        self._z_enabled = value

    @property
    def filter_bandwidth(self) -> str:
        """
        Sensor filter_bandwidth

        +---------------------------------+------------------+
        | Mode                            | Value            |
        +=================================+==================+
        | :py:const:`bma220.ACCEL_32HZ`   | :py:const:`0x05` |
        +---------------------------------+------------------+
        | :py:const:`bma220.ACCEL_64HZ`   | :py:const:`0x04` |
        +---------------------------------+------------------+
        | :py:const:`bma220.ACCEL_125HZ`  | :py:const:`0x03` |
        +---------------------------------+------------------+
        | :py:const:`bma220.ACCEL_250HZ`  | :py:const:`0x02` |
        +---------------------------------+------------------+
        | :py:const:`bma220.ACCEL_500HZ`  | :py:const:`0x01` |
        +---------------------------------+------------------+
        | :py:const:`bma220.ACCEL_1000HZ` | :py:const:`0x00` |
        +---------------------------------+------------------+
        """
        values = (
            "ACCEL_32HZ",
            "ACCEL_64HZ",
            "ACCEL_125HZ",
            "ACCEL_250HZ",
            "ACCEL_500HZ",
            "ACCEL_1000HZ",
        )
        return values[self._filter_bandwidth]

    @filter_bandwidth.setter
    def filter_bandwidth(self, value: int) -> None:
        if value not in filter_bandwidth_values:
            raise ValueError("Value must be a valid filter_bandwidth setting")
        self._filter_bandwidth = value

    @property
    def latched_mode(self) -> str:
        """
        Sensor latched_mode

        +-----------------------------------+-------------------+
        | Mode                              | Value             |
        +===================================+===================+
        | :py:const:`bma220.UNLATCHED`      | :py:const:`0b000` |
        +-----------------------------------+-------------------+
        | :py:const:`bma220.LATCH_FOR_025S` | :py:const:`0b001` |
        +-----------------------------------+-------------------+
        | :py:const:`bma220.LATCH_FOR_050S` | :py:const:`0b010` |
        +-----------------------------------+-------------------+
        | :py:const:`bma220.LATCH_FOR_1S`   | :py:const:`0b011` |
        +-----------------------------------+-------------------+
        | :py:const:`bma220.LATCH_FOR_2S`   | :py:const:`0b100` |
        +-----------------------------------+-------------------+
        | :py:const:`bma220.LATCH_FOR_4S`   | :py:const:`0b101` |
        +-----------------------------------+-------------------+
        | :py:const:`bma220.LATCH_FOR_8S`   | :py:const:`0b110` |
        +-----------------------------------+-------------------+
        | :py:const:`bma220.LATCHED`        | :py:const:`0b111` |
        +-----------------------------------+-------------------+
        """
        values = (
            "UNLATCHED",
            "LATCH_FOR_025S",
            "LATCH_FOR_050S",
            "LATCH_FOR_1S",
            "LATCH_FOR_2S",
            "LATCH_FOR_4S",
            "LATCH_FOR_8S",
            "LATCHED",
        )
        return values[self._latched_mode]

    @latched_mode.setter
    def latched_mode(self, value: int) -> None:
        if value not in latched_mode_values:
            raise ValueError("Value must be a valid latched_mode setting")
        self._latched_mode = value

    @property
    def acceleration(self) -> Tuple[float, float, float]:
        """
        Acceleration
        :return: acceleration
        """
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