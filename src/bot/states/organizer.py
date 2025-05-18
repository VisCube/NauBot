from aiogram.fsm.state import State, StatesGroup


class OrganizerStates(StatesGroup):
    ANSWERING = State()
    POSTING = State()

    CHOOSING_USER = State()
    CHOOSING_ROLE = State()
