Reg = {
    "mic_gain": 0.5,
    "mic_pitch_shift": 0,
    # mic_reverb =
    "mic_lowpass_multi": 1,
    "mic_lowpass_cutoff": 1,
    "soundpad_gain": 1,
    "global_pitch": 1.0,
}
Memo = {
    "soundpad_queue": [],
}


knobs = {
    3: {
        "name": "mic_gain",
        "default": 0.5,
        "min": 0.0,
        "max": 1.5,
    },
    9: {
        "name": "mic_pitch_shift",
        "default": 0.0,
        "min": -2.0,
        "max": 2.0,
    },
    12: {
        "name": "mic_lowpass_multi",
        "default": 1.0,
        "min": 0.0,
        "max": 10.0,
        "log": True,
    },
    13: {
        "name": "mic_lowpass_cutoff",
        "default": 1.0,
        "min": 1.0,
        "max": 5.0,
        "invert": True,
    },
    14: {
        "name": "soundpad_gain",
        "default": 1.0,
        "min": 0.1,
        "max": 2.0,
    },
    15: {
        "name": "global_pitch",
        "default": 1.0,
        "min": 0.8,
        "max": 1.3,
    },
}

pads = {
    38: "bre noise.wav",
    40: "ajr - smallest violin.wav",
}
