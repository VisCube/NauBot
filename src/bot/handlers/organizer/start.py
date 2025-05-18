from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters.command import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.filters.user import OrganizerFilter
from src.bot.keyboards.organizer import get_menu_keyboard
from src.bot.templates.organizer import MESSAGE_START
from src.bot.config import EVENT_NAME

router = Router()


@router.message(CommandStart(), OrganizerFilter())
async def cmd_start(message: Message, db: AsyncSession):
    await message.answer(
        text=MESSAGE_START.format(
            name=message.from_user.full_name,  # TODO ФИО?
            event=EVENT_NAME
        ),
        reply_markup=get_menu_keyboard(),
        parse_mode=ParseMode.HTML
    )
