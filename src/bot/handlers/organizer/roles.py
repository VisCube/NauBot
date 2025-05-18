from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.bot.filters.user import OrganizerFilter
from src.bot.keyboards.organizer import get_role_keyboard
from src.bot.states.organizer import OrganizerStates
from src.bot.templates.organizer import *
from src.bot.templates.participant import NOTIFICATION_REGISTERED

router = Router()


@router.message(F.text == BUTTON_REGISTER, OrganizerFilter())
async def cmd_register(message: Message, state: FSMContext):
    await state.set_state(OrganizerStates.CHOOSING_USER)
    print(message.from_user.id)
    await message.answer(text=PROMPT_USER, parse_mode=ParseMode.HTML)


@router.message(OrganizerStates.CHOOSING_USER, OrganizerFilter())
async def msg_user(message: Message, state: FSMContext):
    await state.set_state(OrganizerStates.CHOOSING_ROLE)
    await state.set_data(dict(user_id=message.text))

    await message.answer(
        text=PROMPT_ROLE,
        reply_markup=get_role_keyboard(),
        parse_mode=ParseMode.HTML
    )


@router.callback_query(OrganizerStates.CHOOSING_ROLE, OrganizerFilter())
async def callback_role(callback: CallbackQuery, state: FSMContext):
    user_id = (await state.get_data()).get("user_id")
    role = callback.data

    # TODO зарегистрировать участника/организатора/волонтёра

    await callback.message.bot.send_message(
        chat_id=user_id,
        text=NOTIFICATION_REGISTERED.format(
            role="организатора" if role == "organizer"
            else "волонтёра" if role == "volunteer"
            else "участника"
        ),
        parse_mode=ParseMode.HTML,
    )

    await state.clear()
    await callback.message.edit_text(
        text=MESSAGE_REGISTERED.format(
            role="Организатор" if role == "organizer"
            else "Волонтёр" if role == "volunteer"
            else "Участник"
        ),
        parse_mode=ParseMode.HTML
    )
