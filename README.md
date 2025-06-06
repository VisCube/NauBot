
## Требования
- Python 3.12 или выше
- Pip (менеджер пакетов Python)
- Telegram Bot Token (получить можно у [@BotFather](https://t.me/BotFather))

## Установка

### 1. Клонирование репозитория
```bash
git clone https://github.com/ваш-пользователь/NauBot.git
cd NauBot
```

### 2. Создание виртуального окружения (рекомендуется)
```bash
# Создание виртуального окружения
python -m venv venv

# Активация виртуального окружения
# Для Windows:
venv\Scripts\activate
# Для Linux/MacOS:
source venv/bin/activate
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Настройка окружения
Создайте файл `.env` в корневой директории проекта со следующим содержимым:
```
BOT_TOKEN=ваш_токен_бота
```
Замените `ваш_токен_бота` на токен, полученный от [@BotFather](https://t.me/BotFather).

## Запуск

### Запуск бота
```bash
python src/main.py
```

## Важное примечание
В текущей версии проекта функционал переключения между ролями пользователя и организатора не полностью реализован. Для тестирования и разработки вам потребуется вносить изменения в файл `src/bot/filters/user.py`:

- Класс `OrganizerFilter` проверяет, является ли пользователь организатором или администратором
- Класс `ParticipantFilter` в настоящий момент содержит заглушку и всегда возвращает `True`

Для переключения между ролями во время тестирования вы можете временно изменить логику в этих фильтрах или напрямую изменить роли пользователей в базе данных.
