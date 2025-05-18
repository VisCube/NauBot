import math

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup
)

from src.bot.templates.participant import *
from src.db.models import Masterclass


def get_menu_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        [
            KeyboardButton(text=BUTTON_SCHEDULE),
            KeyboardButton(text=BUTTON_MAP)
        ],
        [
            KeyboardButton(text=BUTTON_CLASSES),
            KeyboardButton(text=BUTTON_QUESTIONS)
        ]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder=PROMPT_MENU
    )


def get_schedule_keyboard(classes: list) -> InlineKeyboardMarkup:

    last = len(classes)
    if last == 0:
        return InlineKeyboardMarkup(inline_keyboard=[])

    side = max(1, math.ceil(math.sqrt(last)))

    keyboard = [
        [
            InlineKeyboardButton(
                text=classes[j].name,
                callback_data=f"class_{classes[j].id}"
            )
            for j in range(i, min(i + side, last))
        ]
        for i in range(0, last, side)
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_class_keyboard(cls: Masterclass, is_registered: bool = False, is_in_waiting_list: bool = False) -> InlineKeyboardMarkup:
    if not cls:
        return InlineKeyboardMarkup(inline_keyboard=[])
        
    if is_registered or is_in_waiting_list:
        text = BUTTON_DEPART
        callback = f"depart_{cls.id}"
    else:
        text = BUTTON_JOIN if cls.remaining_places > 0 else BUTTON_QUEUE
        callback = f"queue_{cls.id}"

    keyboard = [[InlineKeyboardButton(text=text, callback_data=callback)]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_faq_keyboard(questions: list) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text=f"{q.text[:20]}{'...' if len(q.text) > 20 else ''}", callback_data=f"faq_{q.id}")]
        for q in questions if q is not None
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
