import math

from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup
)

from src.bot.templates.organizer import *


def get_menu_keyboard(prompt: str | None = None) -> ReplyKeyboardMarkup:
    keyboard = [
        [
            KeyboardButton(text=BUTTON_MANAGE),
            KeyboardButton(text=BUTTON_REGISTER),
        ],
        [
            KeyboardButton(text=BUTTON_CLASSES),
            KeyboardButton(text=BUTTON_FEEDBACK)
        ]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder=prompt or PROMPT_MENU
    )


def get_feedback_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text=BUTTON_QUESTION, callback_data="question")],
        [InlineKeyboardButton(text=BUTTON_POLLS, callback_data="polls")],
        [InlineKeyboardButton(text=BUTTON_ACTIVITY, callback_data="activity")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_question_keyboard(question: None) -> InlineKeyboardMarkup:
    # TODO использование модели вопроса

    keyboard = [
        [
            InlineKeyboardButton(
                text=BUTTON_IGNORE,
                callback_data=f"ignore_{0}"
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_role_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="Участник", callback_data="participant")],
        [InlineKeyboardButton(text="Организатор", callback_data="organizer")],
        [InlineKeyboardButton(text="Волонтёр", callback_data="volunteer")]
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )


def get_classes_keyboard(classes: list[None]) -> InlineKeyboardMarkup:
    # TODO использование модели мастер-класса (имя и id)

    last = len(classes)
    side = math.ceil(math.sqrt(last))
    first = InlineKeyboardButton(text=BUTTON_CREATE, callback_data="create")

    keyboard = [[first]] + [
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

    keyboard = [
        [InlineKeyboardButton(text=BUTTON_DELETE, callback_data=f"delete_{0}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
