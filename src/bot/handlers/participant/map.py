from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.filters.user import ParticipantFilter
from src.bot.templates.participant import *
from src.bot.config import MAP_URL

router = Router()


@router.message(F.text == BUTTON_MAP, ParticipantFilter())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()

    await message.answer_photo(
        photo=MAP_URL,
        caption=MESSAGE_MAP.format(),
        parse_mode=ParseMode.HTML
    )
