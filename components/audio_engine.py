import pyaudio
import time
import numpy as np
import wave
from .registry import Reg, Memo
import soxr


CHUNK = 7000
WIDTH = 2
PA_FORMAT = pyaudio.paInt16
DTYPE = np.int16
CHANNELS = 1
RATE = 44100


class MyAudioEngine:
    def __init__(self):
        pa = pyaudio.PyAudio()
        stream = pa.open(
            format=PA_FORMAT,
            channels=CHANNELS,
            rate=RATE,
            frames_per_buffer=CHUNK,
            input=True,
            output=True,
        )
        self.pa = pa
        self.stream = stream
        self.wfs = []

    def process(self):
        # READ
        ## Read from microphone
        chunk = self.stream.read(CHUNK, exception_on_overflow=False)
        chunk = np.frombuffer(chunk, dtype=DTYPE)
        ## Read soundboard wav
        self.wfs += [(wave.open(wf, "rb"), gain) for wf, gain in Memo["soundpad_queue"]]
        Memo["soundpad_queue"] = []

        # EDIT
        ## Microphone
        ### fourier moment
        fourier = np.fft.rfft(chunk)
        fourier_len = fourier.shape[0]
        ### mic pitch
        fourier = np.roll(fourier, s := int(Reg["mic_pitch_shift"]))
        fourier[s if s < 0 else 0 : s if s > 0 else 0] = 0
        ### mic bass boost + distort
        freq_range = int(fourier_len / Reg["mic_lowpass_cutoff"])
        fourier[0:freq_range] *= (multiplier := Reg["mic_lowpass_multi"])
        step = multiplier / freq_range
        i = freq_range
        while multiplier > 1 and i + 1 < fourier_len:
            i += 1
            fourier[i] *= multiplier
            multiplier -= step
        ### Inverse FT
        chunk = np.array(np.fft.irfft(fourier))
        chunk = np.array(chunk * Reg["mic_gain"])

        ## Soundboard
        ## read soundboard wav
        wavs = []
        for i, (wf, gain) in enumerate(self.wfs):
            s_c = wf.readframes(CHUNK)
            if not s_c:
                wf.close()
                self.wfs.pop(i)
                continue
            s_c = np.frombuffer(s_c, dtype=DTYPE)
            if sc_len := s_c.shape[0] > CHUNK:
                s_c = s_c[::2] + s_c[1::2]  # mono-ify
            s_c = s_c * gain
            wavs.append(s_c)
        ## add soundboard wav
        for wav in wavs:
            wav = wav * Reg["soundpad_gain"]
            # wav = soxr.resample(wav, wav.shape[0], CHUNK)
            wav = np.pad(wav, (0, CHUNK - wav.shape[0]), "edge")
            chunk += wav

        ## Global
        ### pitch v2
        chunk = soxr.resample(chunk, CHUNK, int(CHUNK / Reg["global_pitch"]))
        if to_pad := CHUNK - chunk.shape[0] > 0:
            chunk = np.pad(chunk, (0, to_pad), "symmetric")
        else:
            chunk = chunk[:CHUNK]

        # WRITE
        chunk = chunk.astype(DTYPE)
        # print(chunk[1000:1050])
        self.stream.write(chunk.tobytes())

    def run(self):
        print("* routing")
        while 1:
            self.process()
            time.sleep(0.01)

    def end(self):
        self.stream.stop_stream()
        self.stream.close()
        self.pa.terminate()


if __name__ == "__main__":
    a = MyAudioEngine()
    a.run()
