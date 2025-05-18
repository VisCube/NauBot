from aiogram import Router

from .organizer import classes, questions, roles, start
from .participant import classes, map, questions, start


def get_routers() -> list[Router]:
    return [
        organizer.start.router,
        organizer.classes.router,
        organizer.roles.router,
        organizer.questions.router,
        organizer.control_panel.router,

        participant.start.router,
        participant.classes.router,
        participant.map.router,
        participant.questions.router
    ]
