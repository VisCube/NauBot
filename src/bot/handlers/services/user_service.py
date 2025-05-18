from typing import Optional
import qrcode
import io
import base64
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import User, Registration, RoleEnum


async def get_or_create_user(db: AsyncSession,
                             telegram_id: int,
                             full_name: Optional[str] = None,
                             username: Optional[str] = None
                             ) -> User:
    """
    Получить пользователя по telegram_id или создать нового.
    """
    query = select(User).filter(User.tg_id == telegram_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        user = User(tg_id=telegram_id, role=RoleEnum.unregistered)
        db.add(user)
        await db.flush()
        await db.refresh(user)
    await db.commit()
    return user

async def get_masterclass_qr(masterclass_id: int, user_id: int) -> str:
    """
    Генерирует QR-код с информацией о пользователе и событии.
    Возвращает QR-код в формате base64 строки.
    """
    data = f"masterclass:{masterclass_id}|user:{user_id}"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer)
    qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    
    return qr_base64

async def generate_user_qr(user_id: int) -> str:
    """
    Генерирует QR-код только с ID пользователя.
    Возвращает QR-код в формате base64 строки.
    """
    data = f"user:{user_id}"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer)
    qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    
    return qr_base64

async def mark_checked_in(user_id: int, event_id: int, db: AsyncSession) -> bool:
    """
    Отмечает пользователя как посетившего мероприятие.
    Возвращает True в случае успешного обновления, False - если запись не найдена.
    """
    registration_query = select(Registration).filter(
        Registration.user_id == user_id,
        Registration.event_id == event_id
    )
    result = await db.execute(registration_query)
    registration = result.scalar_one_or_none()
    
    if not registration:
        return False
    
    update_stmt = update(Registration).where(
        Registration.user_id == user_id,
        Registration.event_id == event_id
    ).values(checked_in=True)
    
    await db.execute(update_stmt)
    await db.commit()
    
    return True