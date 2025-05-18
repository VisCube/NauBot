from sqlalchemy.future import select
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
        query = select(self.model).filter_by(**filters)
        result = await session.execute(query)
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
        await session.delete(obj)
        await session.commit()
        return True

    @connection
    async def list_all(self, session, **filters):
        query = select(self.model).filter_by(**filters)
        result = await session.execute(query)
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


class MasterclassDAO(BaseDAO):
    def __init__(self):
        super().__init__(Masterclass)


class RegistrationDAO(BaseDAO):
    def __init__(self):
        super().__init__(Registration)


class QuestionDAO(BaseDAO):
    def __init__(self):
        super().__init__(Question)


class SurveyDAO(BaseDAO):
    def __init__(self):
        super().__init__(Survey)


class SurveyOptionDAO(BaseDAO):
    def __init__(self):
        super().__init__(SurveyOption)


class SurveyAnswerDAO(BaseDAO):
    def __init__(self):
        super().__init__(SurveyAnswer)
