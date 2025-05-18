MESSAGE_START = """
Привет, <b>{name}</b>! Добро пожаловать на <b>{event}</b>!
Твоя роль: <b>организатор</b>
"""

PROMPT_MENU = "Выберите пункт меню или введите текст."

BUTTON_MANAGE = "⚙️ Панель управления"
BUTTON_REGISTER = "📝 Добавить участника"
BUTTON_CLASSES = "📖 Мастер-классы"
BUTTON_FEEDBACK = "💬 Обратная связь"

MESSAGE_FEEDBACK = """
Вопросы, ожидающие ответа: <b>{questions}</b>
Проводимые опросы: <b>{polls}</b>
Количество участников: <b>{participants}</b>
"""
BUTTON_QUESTION = "❓ Вопросы участников"
BUTTON_POLLS = "📊 Результаты опросов"
BUTTON_ACTIVITY = "📈 Активность участников"

PROMPT_QUESTION = "Введите ответ на вопрос."
MESSAGE_QUESTION = """
Участник: <b>{participant}</b>
Вопрос: <i>{question}</i>
"""
BUTTON_IGNORE = "⏩ Пропустить вопрос"
MESSAGE_IGNORE = "Вопрос пропущен."
MESSAGE_ANSWERED = "Ответ отправлен участнику."

PROMPT_USER = "Введите ID пользователя в Telegram:"
PROMPT_ROLE = "Выберите роль участника:"
MESSAGE_REGISTERED = "{role} зарегистрирован на мероприятие."

BUTTON_CREATE = "❇️ Создать мастер-класс"
BUTTON_DELETE = "❌ Удалить мастер-класс"

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
ITEM_QUEUED = """
Зарегистрировано: <b>{joined}</b> участников
В очереди: <b>{queued}</b> участников
"""
MESSAGE_CREATED = "Мастер-класс {name} успешно создан."
MESSAGE_DELETED = "Мастер-класс {name} успешно удалён."

PROMPT_NAME = "Введите название мастер-класса:"
PROMPT_DESC = "Введите описание мастер-класса:"
PROMPT_START = "Введите время начала:"
PROMPT_FINAL = "Введите время конца:"
PROMPT_SLOTS = "Введите количество мест:"
