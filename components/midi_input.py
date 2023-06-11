from components.registry import Reg, Memo, knobs, pads


def process_input(e):
    # print(e)
    if e.status == 176:
        conf = knobs[e.data1]
        if conf["min"] > 0:
            val_range = conf["max"] - conf["min"]
        elif conf["max"] < 0:
            val_range = conf["min"] + conf["max"]
        else:
            val_range = abs(conf["min"]) + abs(conf["max"])
        step = val_range / 127
        if conf.get("log"):
            steps = step * e.data2
        else:
            steps = step * e.data2
        if conf.get("invert"):
            new_val = conf["max"] - steps
        else:
            new_val = conf["min"] + steps
        Reg[conf["name"]] = new_val
        str_bld = ""
        for k, v in Reg.items():
            str_bld += f"{k}: {round(v, 3)}    "
        print(str_bld, end="\r")
    if e.data1 == 40:
        Memo["soundpad_queue"].append(
            ("pad_bank/ajr - smallest violin.wav", e.data2 / 127)
        )
