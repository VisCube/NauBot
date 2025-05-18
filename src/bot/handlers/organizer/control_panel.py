from aiogram import F, Router, Bot
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime

from src.bot.filters.user import OrganizerFilter
from src.bot.keyboards.organizer import get_control_panel_keyboard, get_cancel_keyboard, get_menu_keyboard
from src.bot.templates.organizer import *
from src.db.dao.dao import DAOManager
from src.db.models import RoleEnum, Question
from src.db.base import connection

router = Router()


# Определение состояний для разных форм
class PostStates(StatesGroup):
    enter_text = State()


class NotificationStates(StatesGroup):
    enter_text = State()


class ChatLinkStates(StatesGroup):
    enter_link = State()


@router.message(F.text == BUTTON_MANAGE, OrganizerFilter())
async def control_panel_menu(message: Message):
    """Главное меню панели управления"""
    await message.answer(
        text=MESSAGE_CONTROL_PANEL,
        reply_markup=get_control_panel_keyboard(),
        parse_mode=ParseMode.HTML
    )


# Обработчики для написания поста
@router.message(F.text == BUTTON_WRITE_POST, OrganizerFilter())
async def write_post_start(message: Message, state: FSMContext):
    """Начало процесса написания поста"""
    await message.answer(
        text=MESSAGE_WRITE_POST,
        reply_markup=get_cancel_keyboard(),
        parse_mode=ParseMode.HTML
    )
    await state.set_state(PostStates.enter_text)


@router.message(PostStates.enter_text, OrganizerFilter())
@connection
async def process_post_text(message: Message, session, state: FSMContext, bot: Bot):
    """Обработка текста поста и отправка всем пользователям"""
    if message.text == "Отмена":
        await state.clear()
        await control_panel_menu(message)
        return

    post_text = message.text

    # Получаем автора поста для указания в тексте сообщения
    author_name = message.from_user.first_name
    if message.from_user.last_name:
        author_name += f" {message.from_user.last_name}"

    # Формируем красивое сообщение с постом
    post_message = f"""<b>📢 НОВЫЙ ПОСТ</b>

{post_text}

<i>Опубликовано: {author_name}</i>"""

    # Получаем всех пользователей (участников и организаторов)
    from sqlalchemy.future import select
    from src.db.models import User

    query = select(User)  # Выбираем всех пользователей
    result = await session.execute(query)
    users = result.scalars().all()

    sent_count = 0
    error_count = 0

    # Отправляем пост всем пользователям
    for user in users:
        try:
            await bot.send_message(
                chat_id=user.tg_id,
                text=post_message,
                parse_mode=ParseMode.HTML
            )
            sent_count += 1
        except Exception as e:
            error_count += 1
            print(f"Ошибка отправки поста пользователю {user.tg_id}: {e}")

    # Сообщаем организатору о результате рассылки
    result_text = f"✅ Пост успешно опубликован!\n\nОтправлено: {sent_count} пользователям"
    if error_count > 0:
        result_text += f"\nНе удалось отправить: {error_count} пользователям"

    await message.answer(
        text=result_text,
        reply_markup=get_control_panel_keyboard(),
        parse_mode=ParseMode.HTML
    )
    await state.clear()


# Обработчики для отправки уведомлений
@router.message(F.text == BUTTON_SEND_NOTIFICATION, OrganizerFilter())
async def send_notification_start(message: Message, state: FSMContext):
    """Начало процесса отправки уведомления"""
    await message.answer(
        text=MESSAGE_WRITE_NOTIFICATION,
        reply_markup=get_cancel_keyboard(),
        parse_mode=ParseMode.HTML
    )
    await state.set_state(NotificationStates.enter_text)


@router.message(NotificationStates.enter_text, OrganizerFilter())
@connection
async def process_notification_text(message: Message, session, state: FSMContext, bot: Bot):
    """Обработка текста уведомления и отправка всем участникам"""
    if message.text == "Отмена":
        await state.clear()
        await control_panel_menu(message)
        return

    notification_text = message.text

    # Получаем автора уведомления для возможного указания в логах
    author_id = message.from_user.id
    author_name = message.from_user.first_name
    if message.from_user.last_name:
        author_name += f" {message.from_user.last_name}"

    # Формируем красивое сообщение с уведомлением
    notification_message = f"""<b>📣 ВАЖНОЕ УВЕДОМЛЕНИЕ</b>

{notification_text}"""

    # Получаем всех пользователей с ролью участника
    from sqlalchemy.future import select
    from src.db.models import User

    query = select(User)#.where(User.role == RoleEnum.participant)
    result = await session.execute(query)
    users = result.scalars().all()

    sent_count = 0
    error_count = 0

    # Отправляем уведомление всем участникам
    for user in users:
        try:
            await bot.send_message(
                chat_id=user.tg_id,
                text=notification_message,
                parse_mode=ParseMode.HTML
            )
            sent_count += 1
        except Exception as e:
            error_count += 1
            print(f"Ошибка отправки уведомления пользователю {user.tg_id} от организатора {author_id}: {e}")

    # Сообщаем организатору о результате рассылки
    result_text = f"✅ Уведомление успешно отправлено!"

    if users:
        result_text += f"\n\nДоставлено: {sent_count} участникам"
        if error_count > 0:
            result_text += f"\nНе удалось доставить: {error_count} участникам"
    else:
        result_text += "\n\nВнимание: в системе нет зарегистрированных участников"

    await message.answer(
        text=result_text,
        reply_markup=get_control_panel_keyboard(),
        parse_mode=ParseMode.HTML
    )
    await state.clear()


# Обработчики для ввода ссылки на общий чат
@router.message(F.text == BUTTON_ADD_CHAT_LINK, OrganizerFilter())
async def add_chat_link_start(message: Message, state: FSMContext):
    """Начало процесса добавления ссылки на чат"""
    await message.answer(
        text=MESSAGE_ENTER_CHAT_LINK,
        reply_markup=get_cancel_keyboard(),
        parse_mode=ParseMode.HTML
    )
    await state.set_state(ChatLinkStates.enter_link)


#TODO добавляется в бд пока
@router.message(ChatLinkStates.enter_link, OrganizerFilter())
@connection
async def process_chat_link(message: Message, session, state: FSMContext):
    """Обработка введенной ссылки на чат"""
    if message.text == "Отмена":
        await state.clear()
        await control_panel_menu(message)
        return

    link = message.text

    # Проверка валидности ссылки (базовая проверка)
    if not (link.startswith("https://t.me/") or link.startswith("http://t.me/") or
            link.startswith("t.me/") or link.startswith("@")):
        await message.answer(
            text="Введенная ссылка некорректна. Пожалуйста, введите корректную ссылку на Telegram чат.",
            reply_markup=get_cancel_keyboard(),
            parse_mode=ParseMode.HTML
        )
        return

    # Используем Question для хранения ссылки на чат
    # Сначала проверим, есть ли уже запись с ссылкой
    from sqlalchemy.future import select
    query = select(Question).where(Question.answer_text.like("CHAT_LINK:%"))
    result = await session.execute(query)
    chat_link_record = result.scalar_one_or_none()

    if chat_link_record:
        # Обновляем существующую запись
        chat_link_record.answer_text = f"CHAT_LINK:{link}"
        chat_link_record.created_at = datetime.now()
        session.add(chat_link_record)
    else:
        # Создаем новую запись
        chat_link = Question(
            sender_id=message.from_user.id,
            masterclass_id=None,
            is_answered=True,
            answer_text=f"CHAT_LINK:{link}",
            created_at=datetime.now()
        )
        session.add(chat_link)

    await session.commit()

    await message.answer(
        text=MESSAGE_CHAT_LINK_SAVED.format(link=link),
        reply_markup=get_control_panel_keyboard(),
        parse_mode=ParseMode.HTML
    )
    await state.clear()


@router.message(F.text == BUTTON_BACK, OrganizerFilter())
async def return_to_main_menu(message: Message):
    """Возврат в главное меню бота"""
    await message.answer(
        text=MESSAGE_RETURN_TO_MAIN,
        reply_markup=get_menu_keyboard(),
        parse_mode=ParseMode.HTML
    )