from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, Message

from src.bot.filters.user import ParticipantFilter
from src.bot.keyboards.participant import (
    get_class_keyboard,
    get_schedule_keyboard
)
from src.bot.templates.participant import (
    BUTTON_SCHEDULE,
    MESSAGE_CLASS,
    MESSAGE_LEAVE, MESSAGE_SCHEDULE
)

router = Router()


@router.message(F.text == BUTTON_SCHEDULE, ParticipantFilter())
async def cmd_start(message: Message):
    # TODO получение и использование модели мастер-класса

    classes = [None for _ in range(3)]
    lines = [
        MESSAGE_CLASS.format(start="12:34", end="23:45", name="Class")
        for _ in classes
    ]

    await message.answer(
        text=MESSAGE_SCHEDULE.format(classes="".join(lines)),
        reply_markup=get_schedule_keyboard(classes=classes),
        parse_mode=ParseMode.HTML
    )


@router.callback_query(F.data.startswith("class_"), ParticipantFilter())
async def callback_class(callback: CallbackQuery):
    class_id = int(callback.data.split("_")[1])
    class_obj = None  # TODO получение объекта из БД

    await callback.message.edit_text(
        text=f"Мастер-класс: {class_id}",
        reply_markup=get_class_keyboard(class_obj),
        parse_mode=ParseMode.HTML
    )


@router.callback_query(F.data.startswith("leave_"), ParticipantFilter())
async def callback_class(callback: CallbackQuery):
    class_id = int(callback.data.split("_")[1])
    class_obj = None  # TODO получение объекта из БД
    # TODO отмена записи на мастер-класс

    await callback.message.edit_text(
        text=MESSAGE_LEAVE.format(name=f"{class_id}"),
        reply_markup=None,
        parse_mode=ParseMode.HTML
    )
