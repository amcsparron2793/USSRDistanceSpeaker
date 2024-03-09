import os
from machine import Pin, SPI
import mPythonOfficalSDDriver as sdcard_driver
import uos


class UnInitializedCardError(Exception):
    ...


class UnmountedFileSystemError(Exception):
    ...


class SDCard:
    def __init__(self, mount_point: str = '/sd', cs_pin: Pin = Pin(9, Pin.OUT),
                 sck_pin: Pin = Pin(10), mosi_pin: Pin = Pin(11), miso_pin: Pin = Pin(8), **kwargs):
        if kwargs:
            if'test_mode' in kwargs:
                self.test_mode = kwargs['test_mode']
            else:
                self.test_mode = False
            if 'spi_id' in kwargs:
                self.spi_id = kwargs['spi_id']
            else:
                self.spi_id = 1
            if 'auto_mount' in kwargs:
                self.auto_mount = kwargs['auto_mount']
            else:
                self.auto_mount = False
        else:
            self.test_mode = False
            self.spi_id = 1
            self.auto_mount = False

        self.mount_point = mount_point
        # Assign chip select (CS) pin (make sure to start it high - Pin.OUT mode)
        self.cs_pin = cs_pin
        self.sck_pin = sck_pin
        self.mosi_pin = mosi_pin
        self.miso_pin = miso_pin

        self._sd_initialized = False
        self._sd = None
        self._is_mounted = None
        self._file_size = None

        if self.auto_mount:
            self.SD_Initialize()
            self.mount_fs()

    def SD_Initialize(self):
        # Initialize SPI peripheral (start with 1 MHz)
        spi = SPI(self.spi_id,
                  baudrate=1000000,
                  polarity=0,
                  phase=0,
                  bits=8,
                  firstbit=SPI.MSB,
                  sck=self.sck_pin,
                  mosi=self.mosi_pin,
                  miso=self.miso_pin)

        # Initialize SD card
        self._sd = sdcard_driver.SDCard(spi, self.cs_pin)
        self._sd_initialized = True
        return self._sd

    def mount_fs(self):
        if self._sd_initialized:
            # Mount filesystem
            vfs = uos.VfsFat(self._sd)
            # noinspection PyTypeChecker
            uos.mount(vfs, self.mount_point)

            self._is_mounted = True
        else:
            raise UnInitializedCardError("SD Card cannot be mounted before it is initialized.")

    @property
    def file_size(self):
        return self._file_size

    @file_size.setter
    def file_size(self, value):
        if value == 0:
            self._file_size = f"{value} B"
        elif value >= 1000000:
            self._file_size = f"{round(value / 1000000, 2)} MB"
        elif value >= 1000:
            self._file_size = f"{round(value / 1000, 2)} KB"
        else:
            self._file_size = f"{value} B"

    def get_contents(self):
        list_dict_contents = []
        if self._is_mounted:
            for item in os.ilistdir(self.mount_point):
                self.file_size = int(item[-1])

                item = {'name': item[0], 'type': item[1], 'size': self.file_size}

                updated_type = self._int_to_filetype(item)
                item.update(updated_type)

                list_dict_contents.append(item)
            return list_dict_contents
        else:
            raise UnmountedFileSystemError("Filesystem must be mounted first to be read.")

    @staticmethod
    def _int_to_filetype(raw_item):
        if raw_item['type'] == 32768:
            return {'type': 'file'}
        elif raw_item['type'] == 16384:
            return {'type': 'dir'}
        else:
            return {'type': f'unknown ({raw_item["type"]})'}
