from aiogram import Router
from aiogram.filters.command import CommandStart
from aiogram.types import Message

from src.bot.filters.user import OrganizerFilter
from src.bot.keyboards.organizer import get_menu_keyboard
from src.bot.templates.organizer import MESSAGE_START

router = Router()


@router.message(CommandStart(), OrganizerFilter())
async def cmd_start(message: Message):

    await message.answer(
        text=MESSAGE_START.format(
            name=message.from_user.full_name,  # TODO ФИО?
            event="Меро_нейм"  # TODO название меро из конфига
        ),
        reply_markup=get_menu_keyboard()
    )
