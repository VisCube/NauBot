from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Question


async def get_faq_questions(db: AsyncSession) -> list[Question]:
    """Получение часто задаваемых вопросов"""
    result = await db.execute(
        select(Question)
        .where(Question.is_faq == True)
        .order_by(Question.created_at.desc())
    )
    return list(result.scalars().all())


async def get_question_by_id(db: AsyncSession, question_id: int) -> Question | None:
    """Получение вопроса по ID"""
    return await db.get(Question, question_id)


async def create_question(
    db: AsyncSession,
    sender_id: int, 
    text: str, 
    masterclass_id: int = None
) -> Question:
    """Создание нового вопроса"""
    question = Question(
        sender_id=sender_id,
        text=text,
        masterclass_id=masterclass_id,
        is_answered=False,
        is_faq=False
    )
    db.add(question)
    await db.commit()
    await db.refresh(question)
    return question
