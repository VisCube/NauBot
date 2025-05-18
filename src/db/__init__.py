from sqlalchemy.ext.asyncio import AsyncEngine
from .database import engine, Base
from .models import User, Masterclass, Registration, Question, Survey, SurveyOption, SurveyAnswer


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) 