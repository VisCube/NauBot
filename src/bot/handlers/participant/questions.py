from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.filters.user import ParticipantFilter
from src.bot.keyboards.participant import (
    get_faq_keyboard
)
from src.bot.templates.participant import *
from src.bot.handlers.services import question_service

router = Router()


@router.message(F.text == BUTTON_QUESTIONS, ParticipantFilter())
async def cmd_questions(message: Message, state: FSMContext):
    await state.clear()

    questions = [None, None, None]
async def cmd_questions(message: Message, db: AsyncSession):
    questions = await question_service.get_faq_questions(db)

    await message.answer(
        text=MESSAGE_QUESTIONS,
        reply_markup=get_faq_keyboard(questions=questions),
        parse_mode=ParseMode.HTML
    )


@router.callback_query(F.data.startswith("faq_"), ParticipantFilter())
async def callback_faq(callback: CallbackQuery, db: AsyncSession, state: FSMContext):
    await state.clear()

    faq_id = int(callback.data.split("_")[1])
    faq_obj = await question_service.get_question_by_id(db, faq_id)

    await callback.message.edit_text(
        text=MESSAGE_FAQ.format(
            question=faq_obj.text,
            answer=faq_obj.answer_text or ""
        ),
        reply_markup=callback.message.reply_markup,
        parse_mode=ParseMode.HTML
    )


@router.message(ParticipantFilter())
async def cmd_ask_question(message: Message, db: AsyncSession):
    question_text = message.text
    await question_service.create_question(
        db=db,
        sender_id=message.from_user.id,
        text=question_text
    )
async def cmd_questions(message: Message, state: FSMContext):
    await state.clear()

    question = message.text
    # TODO отправка вопроса

    await message.answer(text=MESSAGE_QUESTIONED, parse_mode=ParseMode.HTML)
