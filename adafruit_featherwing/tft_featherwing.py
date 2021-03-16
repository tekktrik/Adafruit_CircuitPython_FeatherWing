# SPDX-FileCopyrightText: 2020 Melissa LeBlanc-Williams for Adafruit Industries
# SPDX-FileCopyrightText: 2020 Foamyguy for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_featherwing.tft_featherwing`
====================================================

Super class for helpers for using the TFT FeatherWing devices
see tft_featherwng_24 and tft_featherwing_35

* Author(s): Melissa LeBlanc-Williams, Foamyguy

Requires:
* adafruit_stmpe610
"""
import board
import digitalio
import displayio
from adafruit_stmpe610 import Adafruit_STMPE610_SPI
import sdcardio
import storage


# pylint: disable-msg=too-few-public-methods, too-many-arguments
class TFTFeatherWing:
    """Class representing an `TFT FeatherWing 2.4
    <https://www.adafruit.com/product/3315>`_.

    """

    def __init__(self, spi=None, cs=None, dc=None, ts_cs=None, sd_cs=None):
        displayio.release_displays()
        if spi is None:
            spi = board.SPI()
        if cs is None:
            cs = board.D9
        if dc is None:
            dc = board.D10

        if ts_cs is None:
            ts_cs = board.D6
        if sd_cs is None:
            sd_cs = board.D5

        ts_cs = digitalio.DigitalInOut(ts_cs)
        self.touchscreen = Adafruit_STMPE610_SPI(spi, ts_cs)

        self._display_bus = displayio.FourWire(spi, command=dc, chip_select=cs)

        self._sdcard = None
        try:
            self._sdcard = sdcardio.SDCard(spi, sd_cs)
            vfs = storage.VfsFat(self._sdcard)
            storage.mount(vfs, "/sd")
        except OSError as error:
            print("No SD card found:", error)
