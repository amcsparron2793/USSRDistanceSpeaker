from machine import Pin, I2S
import ucontextlib
import wave_file
from micropython import mem_info
amp_sck_pin = Pin(11)
amp_word_select = Pin(12)
amp_data_out = Pin(13)
amp_i2s_id = 0
BUFFER_LENGTH_IN_BYTES = 40000
print(mem_info())


def _play_file(wav_data, amp, loop=False, sample_buf=10000):
    # allocate sample array
    # memoryview used to reduce heap allocation
    wav_samples = bytearray(sample_buf)
    wav_samples_mv = memoryview(wav_samples)

    # continuously read audio samples from the WAV file
    # and write them to an I2S DAC
    while True:
        num_read = wav_data.readinto(wav_samples_mv)
        # end of WAV file?
        if num_read == 0:
            # end-of-file, advance to first byte of Data section
            if loop:
                _ = wav_data.seek(44)
            else:
                print("end of file")
                wav_samples = bytearray(sample_buf)
                wav_samples_mv = memoryview(wav_samples)
                buffer_exhaust = int(BUFFER_LENGTH_IN_BYTES / sample_buf)
                for n in range(buffer_exhaust):
                    _ = amp.write(wav_samples_mv[:len(wav_samples) - 1])
                return
        else:
            _ = amp.write(wav_samples_mv[:num_read])


@ucontextlib.contextmanager
def managed_amp(wav_header):
    if wav_header.channels == 1:
        channel_format = I2S.MONO
    elif wav_header.channels == 2:
        channel_format = I2S.STEREO
    else:
        channel_format = I2S.MONO

    amp = I2S(
        amp_i2s_id,
        sck=amp_sck_pin,
        ws=amp_word_select,
        sd=amp_data_out,
        mode=I2S.TX,
        bits=wav_header.bits_per_sample,
        format=channel_format,
        rate=wav_header.sample_rate,
        ibuf=BUFFER_LENGTH_IN_BYTES,
    )
    try:
        yield amp
    finally:
        amp.deinit()


def play(filename, loop=False):
    with open(filename, "rb") as wav:
        wave_header = wave_file.WaveFileHeader.from_file(wav)
        with managed_amp(wave_header) as amp:
            _play_file(wav, amp, loop=loop)
