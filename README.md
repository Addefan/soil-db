# Soil db

## Требования

1. [Python версии не ниже 3.8](https://www.python.org/)
2. [Poetry](https://python-poetry.org/)

##  Инструкции по запуску

1. Вход в виртуальное окружение - `poetry shell`
2. Установка зависимостей - `poetry install`
3. Поднять PostgreSQL с помощью Docker - `docker-compose up -d`
4. Выполнить миграции - `python manage.py migrate` 
5. Для запуска celery на windows - `celery -A notes worker -l info -P gevent`
6. Запуск сервера для разработки на http://localhost:8000 - `python manage.py runserver`

## Обозначения символов в коммитах

- `+` - добавлено
- `-` - удалено
- `=` - изменено
- `!` - исправлено
- `x%` - сделано на x процентов
