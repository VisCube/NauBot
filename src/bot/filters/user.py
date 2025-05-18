from aiogram.filters import BaseFilter
from aiogram.types import Message


class OrganizerFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        # TODO проверка организаторов мероприятия
        return True


class ParticipantFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        # TODO проверка участников мероприятия
        return False
