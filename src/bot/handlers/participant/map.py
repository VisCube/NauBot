from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.filters.user import ParticipantFilter
from src.bot.templates.participant import *

router = Router()


@router.message(F.text == BUTTON_MAP, ParticipantFilter())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()

    # TODO получение ссылки на карту из конфига

    await message.answer_photo(
        photo="https://media.discordapp.net/attachments/1315391589148917842"
              "/1373586263004811325/image.png?ex=682af365&is=6829a1e5&hm"
              "=8ef8aef81908dc829193f9674493adea2bf9a4fe828e3722eae4925c2174fe18&=&format=webp&quality=lossless&width=925&height=913",
        caption=MESSAGE_MAP.format(),
        parse_mode=ParseMode.HTML
    )
