from aiogram import Router
from aiogram.filters.command import CommandStart
from aiogram.types import Message

from src.bot.filters.user import OrganizerFilter, ParticipantFilter

router = Router()


@router.message(CommandStart(), OrganizerFilter())
async def cmd_start(message: Message):
    from src.bot.templates.organizer import MESSAGE_START
    from src.bot.keyboards.organizer import get_menu_keyboard

    await message.answer(
        text=MESSAGE_START.format(
            name=message.from_user.full_name,  # TODO ФИО?
            event="Меро_нейм"  # TODO название меро из конфига
        ),
        reply_markup=get_menu_keyboard()
    )


@router.message(CommandStart(), ParticipantFilter())
async def cmd_start(message: Message):
    from src.bot.templates.participant import MESSAGE_START
    from src.bot.keyboards.participant import get_menu_keyboard

    await message.answer(
        text=MESSAGE_START.format(
            name=message.from_user.full_name,  # TODO ФИО?
            event="Меро_нейм"  # TODO название меро из конфига
        ),
        reply_markup=get_menu_keyboard()
    )


@router.message(CommandStart())
async def cmd_start(message: Message):
    from src.bot.templates.user import MESSAGE_START

    await message.answer(
        text=MESSAGE_START.format(
            name=message.from_user.full_name,
            event="Меро_нейм"  # TODO название меро из конфига
        )
    )
