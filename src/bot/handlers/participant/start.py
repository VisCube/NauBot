from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.filters.user import ParticipantFilter
from src.bot.keyboards.participant import get_menu_keyboard
from src.bot.templates.participant import MESSAGE_START
from src.bot.handlers.services.user_service import get_or_create_user
from src.bot.config import EVENT_NAME

router = Router()


@router.message(CommandStart(), ParticipantFilter())
async def cmd_start(message: Message, db: AsyncSession, state: FSMContext):
    await state.clear()
    await get_or_create_user(
        db=db,
        telegram_id=message.from_user.id,
        full_name=message.from_user.full_name,
        username=message.from_user.username
    )

    await message.answer(
        text=MESSAGE_START.format(
            name=message.from_user.full_name,
            event=EVENT_NAME
        ),
        reply_markup=get_menu_keyboard(),
        parse_mode=ParseMode.HTML
    )
