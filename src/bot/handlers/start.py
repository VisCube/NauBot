from aiogram import Router
from aiogram.filters.command import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.handlers.services.user_service import get_or_create_user

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, db: AsyncSession):
    from src.bot.templates.user import MESSAGE_START
    
    await get_or_create_user(
        db=db,
        telegram_id=message.from_user.id,
        full_name=message.from_user.full_name,
        username=message.from_user.username
    )
    
    await message.answer(
        text=MESSAGE_START.format(
            name=message.from_user.full_name,
            event="Меро_нейм"  # TODO название меро из конфига
        )
    )
