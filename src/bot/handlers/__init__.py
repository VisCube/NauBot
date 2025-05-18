from aiogram import Router

from .organizer import start
from .participant import map, schedule, start


def get_routers() -> list[Router]:
    return [
        organizer.start.router,

        participant.start.router,
        participant.schedule.router,
        participant.map.router
    ]
