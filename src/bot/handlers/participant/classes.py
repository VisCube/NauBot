from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.bot.filters.user import ParticipantFilter
from src.bot.keyboards.participant import (
    get_class_keyboard,
    get_classes_keyboard
)
from src.bot.templates.participant import *

router = Router()


@router.message(F.text == BUTTON_SCHEDULE, ParticipantFilter())
async def cmd_schedule(message: Message, state: FSMContext):
    await state.clear()

    # TODO получение и использование списка мастер-классов,
    #  на которые записан участник

    classes = [None for _ in range(3)]  # TODO получение списка из БД
    lines = [
        ITEM_CLASS.format(start="12:34", end="23:45", name="Class")
        for _ in classes
    ]

    await message.answer(
        text=MESSAGE_SCHEDULE.format(classes="".join(lines)),
        reply_markup=get_classes_keyboard(classes=classes),
        parse_mode=ParseMode.HTML
    )


@router.message(F.text == BUTTON_CLASSES, ParticipantFilter())
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


@router.callback_query(F.data.startswith("class_"), ParticipantFilter())
async def callback_class(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    class_id = int(callback.data.split("_")[1])
    class_obj = None  # TODO получение объекта из БД

    # TODO проверка записи пользователя и количества оставшихся мест
    if False:
        queue_info = ITEM_JOINED
    elif False:
        queue_info = ITEM_AVAILABLE.format(available=5)
    elif False:
        queue_info = ITEM_POSITION.format(position=1)
    else:
        queue_info = ITEM_QUEUE.format(queue=37)

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


@router.callback_query(F.data.startswith("queue_"), ParticipantFilter())
async def callback_queue(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    class_id = int(callback.data.split("_")[1])
    class_obj = None  # TODO получение и использование объекта из БД

    # TODO запись на мастер-класс или очередь к нему

    text = (
        MESSAGE_JOINED.format(name="Cl@ss") if False
        else MESSAGE_QUEUE.format(name="Cl@ss", position=37)
    )

    await callback.message.edit_text(
        text=text,
        reply_markup=None,
        parse_mode=ParseMode.HTML
    )


@router.callback_query(F.data.startswith("depart_"), ParticipantFilter())
async def callback_leave(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    class_id = int(callback.data.split("_")[1])
    class_obj = None  # TODO получение и использование объекта из БД

    # TODO отмена записи или очереди на мастер-класс

    await callback.message.edit_text(
        text=MESSAGE_DEPART.format(name=f"{class_id}"),
        reply_markup=None,
        parse_mode=ParseMode.HTML
    )
