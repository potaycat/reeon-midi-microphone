knobs = {
    3: {
        "name": "mic_gain",
        "default": 1.0,
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
        "max": 300.0,
        "invert": True,
    },
    14: {
        "name": "soundpad_gain",
        "default": 1.0,
        "min": 0.0,
        "max": 2.0,
    },
    15: {
        "name": "global_pitch",
        "default": 1.0,
        "min": 0.8,
        "max": 1.216,
    },
}

pads = {
    38: "bre noise.wav",
    40: "ajr - smallest violin.wav",
}
