import math

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup
)

from src.bot.templates.participant import *


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


def get_classes_keyboard(classes: list[None]) -> InlineKeyboardMarkup:
    # TODO использование модели мастер-класса (имя и id)

    last = len(classes)
    side = math.ceil(math.sqrt(last))

    keyboard = [
        [
            InlineKeyboardButton(
                text=f"Class {j + 1}",
                callback_data=f"class_{j}"
            )
            for j in range(i, min(i + side, last))
        ]
        for i in range(0, last, side)
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_class_keyboard(cls: None) -> InlineKeyboardMarkup:
    # TODO использование модели мастер-класса (id)

    # TODO проверка записи пользователя
    if False or False:
        text = BUTTON_DEPART
        callback = f"depart_{0}"
    else:
        text = BUTTON_JOIN if False else BUTTON_QUEUE
        callback = f"queue_{0}"

    keyboard = [[InlineKeyboardButton(text=text, callback_data=callback)]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
