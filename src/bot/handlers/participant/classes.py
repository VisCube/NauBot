from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.filters.user import ParticipantFilter
from src.bot.keyboards.participant import (
    get_class_keyboard,
    get_schedule_keyboard
)
from src.bot.templates.participant import *
from src.bot.handlers.services.masterclass_service import (
    get_user_masterclasses,
    get_upcoming_masterclasses,
    get_masterclass_details,
    register_user_for_masterclass,
    cancel_user_participation
)
from src.db.models import User, Registration

router = Router()


@router.message(F.text == BUTTON_SCHEDULE, ParticipantFilter())
async def cmd_schedule(message: Message, db: AsyncSession):
    user_masterclasses = await get_user_masterclasses(db, message.from_user.id)
    
    if not user_masterclasses:
        lines = []
    else:
        lines = [
            ITEM_CLASS.format(
                start=item["masterclass"].start_date.strftime("%H:%M"), 
                end=item["masterclass"].end_date.strftime("%H:%M"), 
                name=item["masterclass"].name
            )
            for item in user_masterclasses
        ]
    
    classes = [item["masterclass"] for item in user_masterclasses] if user_masterclasses else []
    
    await message.answer(
        text=MESSAGE_SCHEDULE.format(classes="".join(lines)),
        reply_markup=get_schedule_keyboard(classes=classes),
        parse_mode=ParseMode.HTML
    )


@router.message(F.text == BUTTON_CLASSES, ParticipantFilter())
async def cmd_classes(message: Message, db: AsyncSession):
    classes = await get_upcoming_masterclasses(db)
    
    if not classes:
        lines = []
    else:
        lines = [
            ITEM_CLASS.format(
                start=mc.start_date.strftime("%H:%M"),
                end=mc.end_date.strftime("%H:%M"),
                name=mc.name
            )
            for mc in classes
        ]

    await message.answer(
        text=MESSAGE_CLASSES.format(classes="".join(lines)),
        reply_markup=get_schedule_keyboard(classes=classes),
        parse_mode=ParseMode.HTML
    )


@router.callback_query(F.data.startswith("class_"), ParticipantFilter())
async def callback_class(callback: CallbackQuery, db: AsyncSession):
    class_id = int(callback.data.split("_")[1])
    
    class_obj = await get_masterclass_details(db, class_id)
    
    if not class_obj:
        await callback.answer("Мастер-класс не найден")
        return
    
    reg_query = select(Registration).where(
        Registration.user_id == callback.from_user.id,
        Registration.masterclass_id == class_id
    )
    reg_result = await db.execute(reg_query)
    registration = reg_result.scalar_one_or_none()
    
    if registration and not registration.is_waiting_list:
        queue_info = ITEM_JOINED
    elif class_obj.remaining_places > 0:
        queue_info = ITEM_AVAILABLE.format(available=class_obj.remaining_places)
    elif registration and registration.is_waiting_list:
        position_query = select(Registration).where(
            Registration.masterclass_id == class_id,
            Registration.is_waiting_list == True
        ).order_by(Registration.created_at)
        position_result = await db.execute(position_query)
        registrations = position_result.scalars().all()
        position = next((i + 1 for i, r in enumerate(registrations) if r.user_id == callback.from_user.id), 0)
        queue_info = ITEM_POSITION.format(position=position)
    else:
        queue_query = select(Registration).where(
            Registration.masterclass_id == class_id,
            Registration.is_waiting_list == True
        )
        queue_result = await db.execute(queue_query)
        queue_count = len(queue_result.scalars().all())
        queue_info = ITEM_QUEUE.format(queue=queue_count)

    await callback.message.edit_text(
        text=MESSAGE_CLASS.format(
            name=class_obj.name,
            start=class_obj.start_date.strftime("%H:%M"),
            end=class_obj.end_date.strftime("%H:%M"),
            speaker="",
            description=class_obj.description or "Описание отсутствует",
            queue=queue_info
        ),
        reply_markup=get_class_keyboard(
            cls=class_obj,
            is_registered=registration and not registration.is_waiting_list,
            is_in_waiting_list=registration and registration.is_waiting_list
        ),
        parse_mode=ParseMode.HTML
    )


@router.callback_query(F.data.startswith("queue_"), ParticipantFilter())
async def callback_queue(callback: CallbackQuery, db: AsyncSession):
    class_id = int(callback.data.split("_")[1])
    
    class_obj = await get_masterclass_details(db, class_id)
    
    if not class_obj:
        await callback.answer("Мастер-класс не найден")
        return

    class_name = class_obj.name
    
    result = await register_user_for_masterclass(
        db,
        callback.from_user.id,
        class_id
    )
    
    if result == "masterclass_not_found":
        await callback.answer("Мастер-класс не найден")
        return
    
    if result == "already_registered":
        await callback.answer("Вы уже зарегистрированы на этот мастер-класс")
        return
    
    if result == "already_in_waiting_list":
        await callback.answer("Вы уже в списке ожидания на этот мастер-класс")
        return
    
    if result == "registration_closed":
        await callback.answer("Регистрация на этот мастер-класс закрыта")
        return
    
    if result == "registered":
        text = MESSAGE_JOINED.format(name=class_name)
    else:
        position_query = select(Registration).where(
            Registration.masterclass_id == class_id,
            Registration.is_waiting_list == True
        ).order_by(Registration.created_at)
        position_result = await db.execute(position_query)
        registrations = position_result.scalars().all()
        position = next((i + 1 for i, r in enumerate(registrations) if r.user_id == callback.from_user.id), 0)
        text = MESSAGE_QUEUE.format(name=class_name, position=position)

    await callback.message.edit_text(
        text=text,
        reply_markup=None,
        parse_mode=ParseMode.HTML
    )


@router.callback_query(F.data.startswith("depart_"), ParticipantFilter())
async def callback_leave(callback: CallbackQuery, db: AsyncSession):
    class_id = int(callback.data.split("_")[1])
    
    class_obj = await get_masterclass_details(db, class_id)
    
    if not class_obj:
        await callback.answer("Мастер-класс не найден")
        return
    
    class_name = class_obj.name
    
    result = await cancel_user_participation(
        db,
        callback.from_user.id,
        class_id
    )
    
    if not result:
        await callback.answer("Вы не были зарегистрированы на этот мастер-класс")
        return

    await callback.message.edit_text(
        text=MESSAGE_DEPART.format(name=class_name),
        reply_markup=None,
        parse_mode=ParseMode.HTML
    )
