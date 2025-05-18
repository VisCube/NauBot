from aiogram.filters import BaseFilter
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession


class OrganizerFilter(BaseFilter):
    async def __call__(self, message: Message, db: AsyncSession) -> bool:
        # TODO проверка организаторов мероприятия
        return True


class ParticipantFilter(BaseFilter):
    async def __call__(self, message: Message, db: AsyncSession) -> bool:
        # TODO проверка участников мероприятия
        return False
