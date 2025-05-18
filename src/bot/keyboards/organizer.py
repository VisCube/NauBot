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
    return InlineKeyboardMarkup(
        inline_keyboard=keyboard,
        input_field_placeholder=PROMPT_QUESTION
    )


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
