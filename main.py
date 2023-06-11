from components.audio_engine import MyAudioEngine
from components.midi_input import process_input
import pygame
import pygame.midi
import time

MIDI_DEVICE = 0


def main():
    my_audio_engine = MyAudioEngine()
    pygame.init()
    pygame.fastevent.init()
    pygame.midi.init()

    for i in range(pygame.midi.get_count()):
        device_info = pygame.midi.get_device_info(i)
        print(device_info)

    midi_inp = pygame.midi.Input(MIDI_DEVICE)

    while 1:
        events = pygame.fastevent.get()
        for e in events:
            if e.type in [pygame.midi.MIDIIN]:
                process_input(e)

        if midi_inp.poll():
            midi_evs = pygame.midi.midis2events(
                midi_inp.read(10),
                midi_inp.device_id,
            )
            for ev in midi_evs:
                pygame.fastevent.post(ev)

        my_audio_engine.process()
        time.sleep(0.01)

    pygame.midi.quit()


if __name__ == "__main__":
    main()
