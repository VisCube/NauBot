MESSAGE_START = """
Привет, <b>{name}</b>! Добро пожаловать на <b>{event}</b>!
Твоя роль: <b>участник</b>
"""

PROMPT_MENU = "Выберите пункт меню"
BUTTON_SCHEDULE = "⏰ Моё расписание"
BUTTON_MAP = "🗺️ Карта мероприятия"
BUTTON_CLASSES = "📖 Мастер-классы"
BUTTON_QUESTIONS = "💬 Задать вопрос"

MESSAGE_SCHEDULE = """
Твои мастер-классы:
{classes}
"""
MESSAGE_CLASS = """
<b>{start} — {end}</b>
<i>{name}</i>
"""
MESSAGE_LEAVE = """
Ты больше не записан на мастер-класс {name} :(
"""
BUTTON_LEAVE = "🚪 Покинуть мастер-класс"
