from aiogram.fsm.state import State, StatesGroup


class OrganizerStates(StatesGroup):
    ANSWERING = State()
    POSTING = State()