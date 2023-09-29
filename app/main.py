# Lib imports
import click
from typing import Any, List
from datetime import timedelta
from tqdm import tqdm
from time import sleep

# Local imports
from .notify import notify
from .env import get_environ

@click.group()
@click.option(
    "--notify/--no-notify",
    default=None,
    help="To notify or not after each timer.",
)
@click.option(
    "--sound/--no-sound",
    default=None,
    help="To make a sound or not after a notification",
)
@click.pass_context
def cli(ctx: click.Context, notify: bool | None, sound: bool | None):
    ctx.ensure_object(dict)
    d: dict = ctx.obj
    for key in d.keys():
        d[key] = int(d[key])
    d["NOTIFY"] = notify if notify is not None else bool(d["NOTIFY"])
    d["SOUND"] = sound if sound is not None else bool(d["SOUND"])
    ctx.obj = d

@cli.command()
@click.option(
    "-c",
    "--cycles",
    default=4,
    type=int,
    help="Number of work-break cycles before the long break. Defaults to 4."
)
@click.pass_context
def start(ctx: click.Context, cycles: int):
    deltas: dict[str, List[Any]] = {
        "work": [timedelta(minutes=ctx.obj["WORK_MINUTES"]), 0],
        "short": [timedelta(minutes=ctx.obj["SHORT_BREAK_MINUTES"]), 0],
        "long": [timedelta(minutes=ctx.obj["LONG_BREAK_MINUTES"]), 0],
    }
    timer_cycle = (*(cycles * ["work", "short"]), "long")
    for index in range(len(timer_cycle)):
        timer_type = timer_cycle[index]
        def cycle_name(timer: str):
            return "period" if timer == "work" else "break"
        click.echo(f"{timer_type.title()} {cycle_name(timer_type)}")
        for _ in tqdm(range(deltas[timer_type][0].seconds)):
            sleep(1)
        deltas[timer_type][1] += 1
        notify(
            f"{timer_type.title()} {cycle_name(timer_type)} number {deltas[timer_type][1]}",
            f"Ended! Next you have a {timer_cycle[index + 1]} {cycle_name(timer_cycle[index + 1])}!"
        )
        click.echo()

if __name__ == "__main__":
    cli(obj=get_environ())
