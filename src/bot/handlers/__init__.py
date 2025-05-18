from aiogram import Router

from .organizer import start
from .participant import map, classes, start


def get_routers() -> list[Router]:
    return [
        organizer.start.router,
        organizer.questions.router,

        participant.start.router,
        participant.classes.router,
        participant.map.router,
        participant.questions.router
    ]
