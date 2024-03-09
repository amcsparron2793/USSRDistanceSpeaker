"""

USSRDistanceSpeaker

Plays the USSR anthem when the TOF sensor detects a person

"""
from SDInitialize import SDCard
from ManageAMP import play

from TOF_Sensor import MultiMeasurementUnitTOF
import board
import busio
from time import sleep


# FIXME: commented this out for testing
class UssrTof(MultiMeasurementUnitTOF):
    def print_results(self):
        while True:
            r = self.get_range()  # .print_continuously()
            if r and self.range_has_changed:
                print(r, self.units)
            else:
                # FIXME this never stops printing if r != True
                if self.range_has_changed:  # TODO: and not tof._printed_nothing_detected:
                    print("no reading")
            sleep(0.2)


def initialize_tof():
    print("Starting TOF Sensor")
    i2c = busio.I2C(board.GP1, board.GP0)  # uses board.SCL and board.SDA
    tof = UssrTof(units='mm', i2c=i2c)  # MultiMeasurementUnitTOF.GetUnits(i2c=i2c)
    print("TOF Sensor waiting for command")
    return tof


def get_full_file_path(storage_inst, file_list):
    full_fpath = storage_inst.mount_point + '/5Sec-soviet-anthem.wav'
    found = False

    for x in file_list:
        if x['name'] == '5Sec-soviet-anthem.wav':
            print("found file")
            found = True
    if found:
        pass
    else:
        raise FileNotFoundError(f"Could not find wav file at {full_fpath}")

    return full_fpath


if __name__ == "__main__":
    storage = SDCard(auto_mount=True)
    file_info = storage.get_contents()
    print("SD Initialized")
    full_file_path = get_full_file_path(storage, file_info)

    play(full_file_path)
