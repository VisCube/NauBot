from functools import wraps

from src.db.database import async_session


def connection(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        async with async_session() as session:
            return await func(self, session, *args, **kwargs)
    return wrapper

