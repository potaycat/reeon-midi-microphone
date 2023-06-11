import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

from components.audio_engine import MyAudioEngine
from components.midi_input import process_input
import pygame
import pygame.midi
import time
import pyaudio


def main():
    print("\n** REEON MIDI CONTROLLER FOR MICROPHONE **")
    pygame.init()
    pygame.fastevent.init()
    pygame.midi.init()
    pa = pyaudio.PyAudio()

    print("\nAudio Devices")
    for i in range(pa.get_host_api_info_by_index(0).get("deviceCount")):
        device = pa.get_device_info_by_host_api_device_index(0, i)
        print(
            f"{i}. {device.get('name')} \t| IN: {device.get('maxInputChannels')} OUT: {device.get('maxOutputChannels')}"
        )
    print("\nMIDI Devices")
    for i in range(pygame.midi.get_count()):
        interf, name, inp, outp, opened = pygame.midi.get_device_info(i)
        if inp:
            print(f"{i}. {name.decode('utf-8')}")
    print("\nSelect your devices.")
    in_au = int(input("  Capture audio from: "))
    out_au = int(input("  Output audio to: "))
    in_midi = int(input("  Get MIDI input from: "))

    my_audio_engine = MyAudioEngine(pa, in_au, out_au)
    in_midi = pygame.midi.Input(in_midi)

    print("\n* RUNNING")
    while 1:
        events = pygame.fastevent.get()
        for e in events:
            if e.type in [pygame.midi.MIDIIN]:
                process_input(e)

        if in_midi.poll():
            midi_evs = pygame.midi.midis2events(
                in_midi.read(10),
                in_midi.device_id,
            )
            for ev in midi_evs:
                pygame.fastevent.post(ev)

        my_audio_engine.process()
        time.sleep(0.01)

    pygame.midi.quit()


if __name__ == "__main__":
    main()
