from aiogram.fsm.state import State, StatesGroup


class OrganizerStates(StatesGroup):
    ANSWERING = State()
    POSTING = State()

    CHOOSING_USER = State()
    CHOOSING_ROLE = State()

    CHOOSING_NAME = State()
    CHOOSING_DESC = State()
    CHOOSING_START = State()
    CHOOSING_FINAL = State()
    CHOOSING_SLOTS = State()
