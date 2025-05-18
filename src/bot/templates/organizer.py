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