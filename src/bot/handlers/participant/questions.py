from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, Message

from src.bot.filters.user import ParticipantFilter
from src.bot.keyboards.participant import (
    get_faq_keyboard
)
from src.bot.templates.participant import *

router = Router()


@router.message(F.text == BUTTON_QUESTIONS, ParticipantFilter())
async def cmd_questions(message: Message):
    questions = [None, None, None]

    await message.answer(
        text=MESSAGE_QUESTIONS,
        reply_markup=get_faq_keyboard(questions=questions),
        parse_mode=ParseMode.HTML
    )


@router.callback_query(F.data.startswith("faq_"), ParticipantFilter())
async def callback_faq(callback: CallbackQuery):
    faq_id = int(callback.data.split("_")[1])
    faq_obj = None  # TODO получение и использование объекта из БД

    await callback.message.edit_text(
        text=MESSAGE_FAQ.format(
            question="ПоЧеМу?",
            answer="пОтОмУ!"
        ),
        reply_markup=callback.message.reply_markup,
        parse_mode=ParseMode.HTML
    )


@router.message(ParticipantFilter())
async def cmd_questions(message: Message):
    question = message.text
    # TODO отправка вопроса

    await message.answer(text=MESSAGE_QUESTIONED, parse_mode=ParseMode.HTML)
