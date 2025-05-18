MESSAGE_START = """
Привет, <b>{name}</b>! Добро пожаловать на <b>{event}</b>!
Твоя роль: <b>участник</b>
"""

PROMPT_MENU = "Выберите пункт меню или введите вопрос."
BUTTON_SCHEDULE = "⏰ Моё расписание"
BUTTON_MAP = "🗺️ Карта мероприятия"
BUTTON_CLASSES = "📖 Мастер-классы"
BUTTON_QUESTIONS = "💬 Задать вопрос"

MESSAGE_SCHEDULE = """
Твои мастер-классы:
{classes}
"""
MESSAGE_CLASSES = """
Предстоящие мастер-классы:
{classes}
"""
ITEM_CLASS = """
<b>{start} — {end}</b>
<i>{name}</i>
"""
MESSAGE_CLASS = """
Мастер класс: <b>{name}</b>
Время: <b>{start} — {end}</b>
Спикер: <b>{speaker}</b>
Описание: <i>{description}</i>

{queue}
"""
ITEM_AVAILABLE = "Осталось мест: <b>{available}</b>"
ITEM_JOINED = "Ты записан сюда."
ITEM_QUEUE = "Участников в очереди: <b>{queue}</b>"
ITEM_POSITION = "Твоя позиция в очереди: <b>{position}</b>"

BUTTON_JOIN = "📑 Записаться сюда"
MESSAGE_JOINED = "Ты успешно записан на мастер-класс <b>{name}</b>!"

BUTTON_QUEUE = "⏱️ Встать в очередь"
MESSAGE_QUEUE = """
Теперь ты в очереди на мастер-класс <b>{name}</b>!
Твоя позиция в очереди: {position}
"""

BUTTON_DEPART = "🚪 Отменить запись"
MESSAGE_DEPART = "Ты больше не записан на мастер-класс <b>{name}</b> :("

MESSAGE_MAP = """
<b>Легенда карты:</b>
🚪 — вход/выход
ℹ️ — стойка информации
🧥 — гардероб
📖 — аудитория
🚽 — туалет
🍴 — столовая
"""

MESSAGE_QUESTIONS = "Выбери один из предложенных вопросов или введи свой:"
MESSAGE_FAQ = """
<b>Вопрос</b>: <i>{question}</i>
<b>Ответ</b>: <i>{answer}</i>
"""
MESSAGE_QUESTIONED = "Вопрос отправлен организаторам."

NOTIFICATION_ANSWERED = """
<b>Твой вопрос</b>: <i>{question}</i>
<b>Ответ организатора</b>: <i>{answer}</i>
"""
NOTIFICATION_REGISTERED = """
Поздравляем! Ты зарегистрирован на мероприятие в роли {role}.
"""