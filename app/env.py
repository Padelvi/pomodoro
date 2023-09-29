import os
from typing import Any
from dotenv import load_dotenv

FIELDS: dict[str, Any] = {
    "WORK_MINUTES": 25,
    "SHORT_BREAK_MINUTES": 5,
    "LONG_BREAK_MINUTES": 30,
    "NOTIFY": 1,
    "SOUND": 0,
}

def get_environ() -> dict[str, Any]:
    load_dotenv()
    environ = {key: value for key, value in dict(os.environ).items() if key in FIELDS.keys()}
    for key, default in FIELDS.items():
        if key not in environ.keys():
            environ.update({key: default})
    return environ
