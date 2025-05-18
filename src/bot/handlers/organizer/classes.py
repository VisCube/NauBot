from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.bot.filters.user import OrganizerFilter
from src.bot.keyboards.organizer import (
    get_class_keyboard,
    get_classes_keyboard
)
from src.bot.states.organizer import OrganizerStates
from src.bot.templates.organizer import *

router = Router()


@router.message(F.text == BUTTON_CLASSES, OrganizerFilter())
async def cmd_classes(message: Message, state: FSMContext):
    await state.clear()

    # TODO получение и использование списка предстоящих мастер-классов

    classes = [None for _ in range(5)]  # TODO получение списка из БД
    lines = [
        ITEM_CLASS.format(start="12:34", end="23:45", name="Cl@ss")
        for _ in classes
    ]

    await message.answer(
        text=MESSAGE_CLASSES.format(classes="".join(lines)),
        reply_markup=get_classes_keyboard(classes=classes),
        parse_mode=ParseMode.HTML
    )


@router.callback_query(F.data.startswith("class_"), OrganizerFilter())
async def callback_class(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    class_id = int(callback.data.split("_")[1])
    class_obj = None  # TODO получение и использование объекта из БД

    queue_info = ITEM_QUEUED.format(
        joined=13,
        queued=37,
    )

    await callback.message.edit_text(
        text=MESSAGE_CLASS.format(
            name="Cl@ss",
            start="12:34",
            end="23:45",
            speaker="Гигачад",
            description="Очень крутой мастер-класс",
            queue=queue_info
        ),
        reply_markup=get_class_keyboard(cls=class_obj),
        parse_mode=ParseMode.HTML
    )


@router.callback_query(F.data == "create", OrganizerFilter())
async def callback_create(callback: CallbackQuery, state: FSMContext):
    await state.set_state(OrganizerStates.CHOOSING_NAME)

    await callback.message.edit_text(
        text=PROMPT_NAME,
        parse_mode=ParseMode.HTML,
    )


@router.message(OrganizerStates.CHOOSING_NAME, OrganizerFilter())
async def msg_name(message: Message, state: FSMContext):
    await state.set_state(OrganizerStates.CHOOSING_DESC)
    data = await state.get_data()
    data.update(dict(name=message.text))
    await state.set_data(data)

    await message.answer(
        text=PROMPT_DESC,
        parse_mode=ParseMode.HTML,
    )


@router.message(OrganizerStates.CHOOSING_DESC, OrganizerFilter())
async def msg_desc(message: Message, state: FSMContext):
    await state.set_state(OrganizerStates.CHOOSING_START)
    data = await state.get_data()
    data.update(dict(desc=message.text))
    await state.set_data(data)

    await message.answer(
        text=PROMPT_START,
        parse_mode=ParseMode.HTML,
    )


@router.message(OrganizerStates.CHOOSING_START, OrganizerFilter())
async def msg_start(message: Message, state: FSMContext):
    await state.set_state(OrganizerStates.CHOOSING_FINAL)
    data = await state.get_data()
    data.update(dict(start=message.text))
    await state.set_data(data)

    await message.answer(
        text=PROMPT_FINAL,
        parse_mode=ParseMode.HTML,
    )


@router.message(OrganizerStates.CHOOSING_FINAL, OrganizerFilter())
async def msg_final(message: Message, state: FSMContext):
    await state.set_state(OrganizerStates.CHOOSING_SLOTS)
    data = await state.get_data()
    data.update(dict(final=message.text))
    await state.set_data(data)

    await message.answer(
        text=PROMPT_SLOTS,
        parse_mode=ParseMode.HTML,
    )


@router.message(OrganizerStates.CHOOSING_SLOTS, OrganizerFilter())
async def msg_slots(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data.get("name")
    desc = data.get("desc")
    start = data.get("start")
    final = data.get("final")
    slots = message.text

    # TODO запись мероприятия в базу
    # TODO рассылка уведомлений

    await state.clear()
    await message.answer(
        text=MESSAGE_CREATED.format(name=name),
        parse_mode=ParseMode.HTML,
    )


@router.callback_query(F.data.startswith("delete_"), OrganizerFilter())
async def callback_delete(callback: CallbackQuery, state: FSMContext):
    await state.set_state()

    class_id = int(callback.data.split("_")[1])
    class_obj = None  # TODO получение и использование объекта из БД

    # TODO удаление мастер-класса

    await callback.message.edit_text(
        text=MESSAGE_DELETED.format(name="Cl@ss"),
        parse_mode=ParseMode.HTML,
    )
