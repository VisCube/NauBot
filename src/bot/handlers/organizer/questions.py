from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.bot.filters.user import OrganizerFilter
from src.bot.keyboards.organizer import (
    get_feedback_keyboard,
    get_question_keyboard
)
from src.bot.states.organizer import OrganizerStates
from src.bot.templates.organizer import *
from src.bot.templates.participant import NOTIFICATION_ANSWERED

router = Router()


@router.message(F.text == BUTTON_FEEDBACK, OrganizerFilter())
async def cmd_feedback(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(
        text=MESSAGE_FEEDBACK.format(
            questions=7,
            polls=3,
            participants=37,
        ),
        reply_markup=get_feedback_keyboard(),
        parse_mode=ParseMode.HTML
    )


@router.callback_query(F.data == "question", OrganizerFilter())
async def callback_question(callback: CallbackQuery, state: FSMContext):
    question = None  # TODO получить следующий вопрос из БД

    await state.set_state(OrganizerStates.ANSWERING)
    await state.set_data(dict(question_id=13))

    await callback.message.edit_text(
        text=MESSAGE_QUESTION.format(
            participant="Участник №37",
            question="ЗаЧеМ?"
        ),
        reply_markup=get_question_keyboard(question=question),
        parse_mode=ParseMode.HTML
    )


@router.callback_query(F.data.startswith("ignore_"), OrganizerFilter())
async def callback_ignore(callback: CallbackQuery, state: FSMContext):
    question_id = int(callback.data.split("_")[1])
    question = None  # TODO получение и использование вопроса из БД

    # TODO отметить вопрос как проигнорированный

    await state.clear()
    await callback.message.edit_text(
        text=MESSAGE_IGNORE,
        reply_markup=get_feedback_keyboard(),
        parse_mode=ParseMode.HTML,
    )


@router.message(OrganizerStates.ANSWERING, OrganizerFilter())
async def input_answer(message: Message, state: FSMContext):
    question_id = (await state.get_data()).get("question_id")
    question = None  # TODO получение и использование вопроса из БД
    # TODO пометить вопрос как отвеченный

    answer = message.text
    user_id = message.from_user.id

    await message.bot.send_message(
        chat_id=user_id,
        text=NOTIFICATION_ANSWERED.format(
            question="ВоПрОс",
            answer=answer
        ),
        parse_mode=ParseMode.HTML,
    )

    await state.clear()
    await message.answer(
        text=MESSAGE_ANSWERED,
        reply_markup=get_feedback_keyboard(),
        parse_mode=ParseMode.HTML,
    )
