from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from src.db.models import *
from src.db.base import connection


class BaseDAO:
    def __init__(self, model):
        self.model = model

    @connection
    async def add(self, session, obj):
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    @connection
    async def get(self, session, **filters):
        stmt = select(self.model).filter_by(**filters)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @connection
    async def update(self, session, obj, **values):
        for key, value in values.items():
            setattr(obj, key, value)
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    @connection
    async def delete(self, session, obj):
        if not obj:
            return False
        await session.delete(obj)
        await session.commit()
        return True

    @connection
    async def list_all(self, session, **filters):
        stmt = select(self.model).filter_by(**filters)
        result = await session.execute(stmt)
        return result.scalars().all()


class DAOManager:
    def __init__(self):
        self.users = UserDAO()
        self.masterclasses = MasterclassDAO()
        self.registrations = RegistrationDAO()
        self.questions = QuestionDAO()
        self.surveys = SurveyDAO()
        self.survey_options = SurveyOptionDAO()
        self.survey_answers = SurveyAnswerDAO()


class UserDAO(BaseDAO):
    def __init__(self):
        super().__init__(User)

    @connection
    async def add(self, session, user: User):
        stmt = select(User).filter_by(tg_id=user.tg_id)
        result = await session.execute(stmt)
        if not result.scalar_one_or_none():
            session.add(user)
            await session.commit()
            await session.refresh(user)
        return result


class MasterclassDAO(BaseDAO):
    def __init__(self):
        super().__init__(Masterclass)

    @connection
    async def get(self, session, **filters):
        stmt = select(Masterclass).filter_by(**filters).options(joinedload(Masterclass.registrations))
        result = await session.execute(stmt)
        return result.unique().scalar_one_or_none()

    @connection
    async def list_all(self, session, **filters):
        stmt = select(Masterclass).options(joinedload(Masterclass.registrations))
        result = await session.execute(stmt)
        return result.unique().scalars().all()


class RegistrationDAO(BaseDAO):
    def __init__(self):
        super().__init__(Registration)

    @connection
    async def add(self, session, registration: Registration):
        stmt = select(Registration).filter_by(user_id=registration.user_id,
                                              masterclass_id=registration.masterclass_id)
        result = await session.execute(stmt)
        if not result.scalar_one_or_none():
            session.add(registration)
            await session.commit()
            await session.refresh(registration)
        return result


class QuestionDAO(BaseDAO):
    def __init__(self):
        super().__init__(Question)

    @connection
    async def get_oldest_unanswered(self, session):
        stmt = (select(Question)
                .filter_by(is_answered=False)
                .order_by(Question.created_at.asc())
                .limit(1))
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


class SurveyDAO(BaseDAO):
    def __init__(self):
        super().__init__(Survey)


class SurveyOptionDAO(BaseDAO):
    def __init__(self):
        super().__init__(SurveyOption)


class SurveyAnswerDAO(BaseDAO):
    def __init__(self):
        super().__init__(SurveyAnswer)
