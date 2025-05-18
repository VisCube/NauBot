from datetime import datetime
from typing import List, Optional, Dict, Any, Union, Literal

from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.db.models import Masterclass, Registration, User
from src.bot.handlers.services.user_service import get_or_create_user


async def get_user_masterclasses(db: AsyncSession, telegram_user_id: int) -> List[Dict[str, Any]]:
    query = select(Masterclass).options(selectinload(Masterclass.registrations)).join(Registration, Registration.masterclass_id == Masterclass.id).where(
        Registration.user_id == telegram_user_id
    ).order_by(Masterclass.start_date)
    
    result = await db.execute(query)
    masterclasses = result.scalars().all()
    
    schedule = []
    for mc in masterclasses:
        reg_query = select(Registration).where(
            Registration.user_id == telegram_user_id,
            Registration.masterclass_id == mc.id
        )
        reg_result = await db.execute(reg_query)
        registration = reg_result.scalar_one_or_none()
        
        status = "registered" if not registration.is_waiting_list else "waiting_list"
        item = {"masterclass": mc, "status": status}
        
        if status == "waiting_list":
            position_query = select(Registration).where(
                Registration.masterclass_id == mc.id,
                Registration.is_waiting_list == True
            ).order_by(Registration.created_at)
            position_result = await db.execute(position_query)
            registrations = position_result.scalars().all()
            position = next((i + 1 for i, r in enumerate(registrations) if r.user_id == telegram_user_id), 0)
            item["position"] = position
            
        schedule.append(item)
    
    return schedule


async def get_upcoming_masterclasses(db: AsyncSession) -> List[Masterclass]:
    now = datetime.now()
    
    query = select(Masterclass).options(selectinload(Masterclass.registrations)).where(
        Masterclass.start_date > now
    ).order_by(Masterclass.start_date)
    
    result = await db.execute(query)
    return result.scalars().all()


async def get_masterclass_details(db: AsyncSession, masterclass_id: int) -> Optional[Masterclass]:
    query = select(Masterclass).options(
        selectinload(Masterclass.registrations),
        selectinload(Masterclass.speaker)
    ).where(Masterclass.id == masterclass_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


RegistrationType = Literal[
    "registered", "waiting_list", "capacity_full", "already_registered",
    "already_in_waiting_list", "masterclass_not_found", "registration_closed", "error"
]


async def register_user_for_masterclass(
        db: AsyncSession,
        telegram_user_id: int,
        masterclass_id: int
) -> RegistrationType:
    user = await get_or_create_user(db, telegram_user_id)
    masterclass = await get_masterclass_details(db, masterclass_id)
    
    if not masterclass:
        return "masterclass_not_found"
    
    if datetime.now() >= masterclass.start_date:
        return "registration_closed"
    
    existing_reg_query = select(Registration).where(
        Registration.user_id == telegram_user_id,
        Registration.masterclass_id == masterclass_id
    )
    existing_reg_result = await db.execute(existing_reg_query)
    existing_reg = existing_reg_result.scalar_one_or_none()
    
    if existing_reg:
        if existing_reg.is_waiting_list:
            return "already_in_waiting_list"
        else:
            return "already_registered"
    
    reg_count_query = select(func.count()).select_from(Registration).where(
        Registration.masterclass_id == masterclass_id,
        Registration.is_waiting_list == False
    )
    reg_count_result = await db.execute(reg_count_query)
    registered_count = reg_count_result.scalar_one()
    
    is_waiting = registered_count >= masterclass.capacity
    
    registration = Registration(
        user_id=telegram_user_id,
        masterclass_id=masterclass_id,
        is_waiting_list=is_waiting
    )
    
    db.add(registration)
    await db.commit()
    
    return "waiting_list" if is_waiting else "registered"


async def cancel_user_participation(db: AsyncSession, telegram_user_id: int, masterclass_id: int) -> bool:
    query = select(Registration).where(
        Registration.user_id == telegram_user_id,
        Registration.masterclass_id == masterclass_id
    )
    result = await db.execute(query)
    registration = result.scalar_one_or_none()
    
    if not registration:
        return False
    
    was_registered = not registration.is_waiting_list
    
    await db.delete(registration)
    await db.commit()
    
    if was_registered:
        waiting_query = select(Registration).where(
            Registration.masterclass_id == masterclass_id,
            Registration.is_waiting_list == True
        ).order_by(Registration.created_at)
        waiting_result = await db.execute(waiting_query)
        first_waiting = waiting_result.scalar_one_or_none()
        
        if first_waiting:
            first_waiting.is_waiting_list = False
            await db.commit()
    
    return True 