from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from src.bot.templates.organizer import *


def get_menu_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        [
            KeyboardButton(text=BUTTON_MANAGE),
            KeyboardButton(text=BUTTON_MAP)
        ],
        [
            KeyboardButton(text=BUTTON_CLASSES),
            KeyboardButton(text=BUTTON_FEEDBACK)
        ]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder=PROMPT_MENU
    )
