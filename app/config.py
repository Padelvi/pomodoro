from os import listdir
import json

FIELDS: dict[str, int | float] = {
    "WORK_MINUTES": 30,
    "SHORT_BREAK_MINUTES": 5,
    "LONG_BREAK_MINUTES": 30,
    "CYCLES": 4,
    "NOTIFY": 1,
    "SOUND": 0,
    "VOLUME": 0.9,
}

def get_config(full_filepath: str = "config.json") -> dict[str, int | float]:
    if "/" in full_filepath:
        filepath = full_filepath.split("/")
        path_to_search = "/".join(filepath[:-1])
    else:
        filepath = [full_filepath,]
        path_to_search = None
    if filepath[-1] not in listdir(path_to_search):
        open(full_filepath, "x")
        with open(full_filepath, "w") as config_raw:
            json.dump(FIELDS, config_raw)
        return FIELDS
    with open(full_filepath, "r") as config_raw:
        try:
            config = json.load(config_raw)
        except json.decoder.JSONDecodeError:
            with open(full_filepath, "w") as config_raw:
                json.dump(FIELDS, config_raw)
            return FIELDS
        for key, default in FIELDS.items():
            if key not in config.keys():
                config.update({key: default})
        return config

def pass_config(config: dict):
    for key in config.keys():
        config[key] = int(config[key])
    config["NOTIFY"] = bool(config["NOTIFY"])
    config["SOUND"] = bool(config["SOUND"])
    return config
