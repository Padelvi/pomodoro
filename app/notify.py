from pynotifier import Notification, NotificationClient
from pynotifier.backends import platform

c = NotificationClient()
c.register_backend(platform.Backend())

def notify(title: str, message: str) -> None:
    c.notify_all(Notification(title=title, message=message))
