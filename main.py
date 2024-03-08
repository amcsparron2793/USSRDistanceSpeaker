"""

USSRDistanceSpeaker

Plays the USSR anthem when the TOF sensor detects a person

"""
from SDInitialize import SD_Initialize


if __name__ == "__main__":
    from ManageAMP import play

    mnt_point = SD_Initialize()
    print('\t\tSD initialized\n')
    print(f"\tFiles found at mount point: \'{mnt_point}\':")
    from os import listdir
    for f in listdir(mnt_point):
        print(f"\t\t{f}")
    # FIXME: this is what causes the crashing/weird behavior...
    # play(mnt_point + '/BETTERsoviet-anthem.wav')
