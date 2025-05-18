from aiogram.filters import BaseFilter
from aiogram.types import Message
from sqlalchemy.future import select

from src.db.models import User, RoleEnum
from src.db.database import async_session


class OrganizerFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        """
        Проверяет, является ли пользователь организатором или администратором.

        :param message: Сообщение от пользователя
        :return: True, если пользователь имеет роль организатора или админа
        """
        async with async_session() as session:
            # Получаем пользователя по telegram id
            query = select(User).where(User.tg_id == message.from_user.id)
            result = await session.execute(query)
            user = result.scalar_one_or_none()

            # Проверяем роль пользователя
            if user and (user.role == RoleEnum.organizer or user.role == RoleEnum.admin):
                return True

            return False


class ParticipantFilter(BaseFilter):
    async def __call__(self, message: Message, db: AsyncSession) -> bool:
        # TODO проверка участников мероприятия
        return True
