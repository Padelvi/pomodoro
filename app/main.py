# Lib imports
import click
from typing import Any, List
from datetime import datetime, timedelta
from nptime import nptime
from tqdm import tqdm
from time import sleep
from pynotifier import Notification, NotificationClient
from pynotifier.backends import platform

# Local imports
from .config import get_config, pass_config

def notify(
    title: str,
    message: str,
) -> None:
    client = NotificationClient()
    client.register_backend(platform.Backend())
    client.notify_all(Notification(title=title, message=message))

def now() -> nptime:
    time = datetime.now().time()
    return nptime(hour=time.hour, minute=time.minute, second=time.second)

@click.command()
def timer():
    config = pass_config(get_config())
    deltas: dict[str, List[Any]] = {
        "work": [timedelta(minutes=config["WORK_MINUTES"]), 0],
        "short": [timedelta(minutes=config["SHORT_BREAK_MINUTES"]), 0],
        "long": [timedelta(minutes=config["LONG_BREAK_MINUTES"]), 0],
    }
    timer_cycle = (*(config["CYCLES"] * ["work", "short"]), "long")
    for index in range(len(timer_cycle)):
        timer_type = timer_cycle[index]
        ends = now() + deltas[timer_type][0]
        def cycle_name(timer: str):
            return "period" if timer == "work" else "break"
        click.echo(f"{timer_type.title()} {cycle_name(timer_type)}")
        click.echo(f"Ends at {str(ends)}")
        for _ in tqdm(range(deltas[timer_type][0].seconds)):
            sleep(1)
        deltas[timer_type][1] += 1
        notify(
            f"{timer_type.title()} {cycle_name(timer_type)} number {deltas[timer_type][1]}",
            f"Ended! Next you have a {timer_cycle[index + 1]} {cycle_name(timer_cycle[index + 1])}!",
        )
        click.echo()

if __name__ == "__main__":
    timer()
