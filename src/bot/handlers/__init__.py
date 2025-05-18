from aiogram import Router

from .organizer import start
from .participant import classes, map, questions, start


def get_routers() -> list[Router]:
    return [
        organizer.start.router,

        participant.start.router,
        participant.classes.router,
        participant.map.router,
        participant.questions.router
    ]
