# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`bma220_slope`
================================================================================

BMA220 Slope Bosch Circuitpython Driver library


* Author(s): Jose D. Montoya


"""
# pylint: disable=useless-parent-delegation,no-name-in-module

from micropython import const
from adafruit_register.i2c_bit import RWBit, ROBit
from bma220.bma220 import BMA220


__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/jposada202020/CircuitPython_BMA220.git"

_CONF = const(0x1A)
_INTERRUPTS = const(0x18)

# Slope Axis Enabled Values
SLOPE_X_DISABLED = const(0b0)
SLOPE_X_ENABLED = const(0b1)
SLOPE_Y_DISABLED = const(0b0)
SLOPE_Y_ENABLED = const(0b1)
SLOPE_Z_DISABLED = const(0b0)
SLOPE_Z_ENABLED = const(0b1)
slope_axis_enabled_values = (SLOPE_X_DISABLED, SLOPE_X_ENABLED)


class BMA220_SLOPE(BMA220):
    """
    BMA220 Slope mode class
    """

    _slope_z_enabled = RWBit(_CONF, 3)
    _slope_y_enabled = RWBit(_CONF, 4)
    _slope_x_enabled = RWBit(_CONF, 5)
    _slope_int = ROBit(_INTERRUPTS, 0)

    def __init__(self, i2c_bus):
        super().__init__(i2c_bus)

    @property
    def slope_x_enabled(self) -> str:
        """
        Sensor slope_x_enabled

        +-------------------------------------------+-----------------+
        | Mode                                      | Value           |
        +===========================================+=================+
        | :py:const:`bma220_slope.SLOPE_X_DISABLED` | :py:const:`0b0` |
        +-------------------------------------------+-----------------+
        | :py:const:`bma220_slope.SLOPE_X_ENABLED`  | :py:const:`0b1` |
        +-------------------------------------------+-----------------+
        """
        values = (
            "SLOPE_X_DISABLED",
            "SLOPE_X_ENABLED",
        )
        return values[self._slope_x_enabled]

    @slope_x_enabled.setter
    def slope_x_enabled(self, value: int) -> None:
        if value not in slope_axis_enabled_values:
            raise ValueError("Value must be a valid slope_x_enabled setting")
        self._slope_x_enabled = value

    @property
    def slope_y_enabled(self) -> str:
        """
        Sensor y_enabled

        +-------------------------------------------+-----------------+
        | Mode                                      | Value           |
        +===========================================+=================+
        | :py:const:`bma220_slope.SLOPE_Y_DISABLED` | :py:const:`0b0` |
        +-------------------------------------------+-----------------+
        | :py:const:`bma220_slope.SLOPE_Y_ENABLED`  | :py:const:`0b1` |
        +-------------------------------------------+-----------------+
        """
        values = (
            "SLOPE_Y_DISABLED",
            "SLOPE_Y_ENABLED",
        )
        return values[self._slope_y_enabled]

    @slope_y_enabled.setter
    def slope_y_enabled(self, value: int) -> None:
        if value not in slope_axis_enabled_values:
            raise ValueError("Value must be a valid slope_y_enabled setting")
        self._slope_y_enabled = value

    @property
    def slope_z_enabled(self) -> str:
        """
        Sensor slope_z_enabled

        +-------------------------------------------+-----------------+
        | Mode                                      | Value           |
        +===========================================+=================+
        | :py:const:`bma220_slope.SLOPE_Z_DISABLED` | :py:const:`0b0` |
        +-------------------------------------------+-----------------+
        | :py:const:`bma220_slope.SLOPE_Z_ENABLED`  | :py:const:`0b1` |
        +-------------------------------------------+-----------------+
        """
        values = (
            "SLOPE_Z_DISABLED",
            "SLOPE_Z_ENABLED",
        )
        return values[self._slope_z_enabled]

    @slope_z_enabled.setter
    def slope_z_enabled(self, value: int) -> None:
        if value not in slope_axis_enabled_values:
            raise ValueError("Value must be a valid slope_z_enabled setting")
        self._slope_z_enabled = value

    @property
    def slope_interrupt(self) -> bool:
        """
        Sensor slope_z_enabled

        """

        return self._slope_int
