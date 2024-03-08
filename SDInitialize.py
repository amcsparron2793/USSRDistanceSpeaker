from machine import Pin, SPI
import mPythonOfficalSDDriver as sdcard
import uos


def SD_Initialize(mount_point: str = "/sd", **kwargs):
    def _SD_Test():
        # Create a file and write something to it
        with open((mount_point + "/test01.txt"), "w") as file:
            file.write("Hello, SD World!\r\n")
            file.write("This is a test\r\n")

        # Open the file we just created and read from it
        with open((mount_point + "/test01.txt"), "r") as file:
            data = file.read()
            print(data)

    test_mode = False

    if kwargs:
        if 'test' in kwargs:
            test_mode = kwargs['test']
        else:
            pass
    # Assign chip select (CS) pin (and start it high)
    cs = Pin(9, Pin.OUT)

    # Initialize SPI peripheral (start with 1 MHz)
    spi = SPI(1,
              baudrate=1000000,
              polarity=0,
              phase=0,
              bits=8,
              firstbit=SPI.MSB,
              sck=Pin(10),
              mosi=Pin(11),
              miso=Pin(8))

    # Initialize SD card
    sd = sdcard.SDCard(spi, cs)

    # Mount filesystem
    vfs = uos.VfsFat(sd)
    # noinspection PyTypeChecker
    uos.mount(vfs, mount_point)

    if test_mode:
        _SD_Test()

    return mount_point
