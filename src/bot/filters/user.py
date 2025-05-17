from aiogram.filters import BaseFilter
from aiogram.types import Message


class OrganizerFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        # TODO проверка организаторов мероприятия
        return False


class ParticipantFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        # TODO проверка участников мероприятия
        return True
