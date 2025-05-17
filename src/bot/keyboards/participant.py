from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

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

def get_schedule_keyboard(events: list[str]) -> ReplyKeyboardMarkup:
    keyboard = [[KeyboardButton(text=event)] for event in events]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder=PROMPT_MENU
    )