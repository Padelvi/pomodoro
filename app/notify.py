import os
from pynotifier import Notification, NotificationClient
from pynotifier.backends import platform
from pipewire_python.controller import Controller

notify_client = NotificationClient()
notify_client.register_backend(platform.Backend())

class NotValidAudioException(Exception):
    def __init__(self, message="Not valid audio. No reason specified.") -> None:
        super().__init__(message)

def activate_pipewire() -> tuple[Controller | None, str | None]:
    files = os.listdir("assets")
    filenames = tuple(map(lambda file: os.path.splitext(file)[0], files))
    valid_extensions = [".wav", ".mp3"]
    audio = None
    for filename_index in range(len(filenames)):
        if filenames[filename_index] == "sound":
            if audio is not None:
                raise NotValidAudioException("More than one file called 'audio'.")
            else:
                audio = files[filename_index]
                if os.path.splitext(audio)[1] not in valid_extensions:
                    raise NotValidAudioException("Extension not valid for audio file.")
    pw = None if audio is None else Controller()
    return pw, audio

def notify(
    title: str,
    message: str,
    pw: Controller | None = None,
    audio: str | None = None
) -> None:
    notify_client.notify_all(Notification(title=title, message=message))
    if pw is not None:
        if audio is None:
            raise NotValidAudioException("Controller provided but not audio")
        else:
            pw.playback(f"assets/audio/{audio}")
