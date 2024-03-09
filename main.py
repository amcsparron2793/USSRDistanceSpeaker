"""

USSRDistanceSpeaker

Plays the USSR anthem when the TOF sensor detects a person

"""
from SDInitialize import SDCard


if __name__ == "__main__":
    #from ManageAMP import play
    storage = SDCard(auto_mount=True)
    file_list = storage.get_contents()

    # FIXME: this is what causes the crashing/weird behavior...
    # play(mnt_point + '/BETTERsoviet-anthem.wav')
    for x in file_list:
        print(x)
