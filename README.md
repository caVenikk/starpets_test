# Тестовое для starpets.gg

## Веб-приложение для управления пользователями

Реализовано на Flask. БД - SQLite, aiosqlite.

## Запуск

1. Переменные окружения

   ```shell
   cp .env.dist .env
   ```
   В файле .env определить переменные:
    * Название файла с БД,
    * API-токен для работы с OpenWeatherAPI.

2. Локальный запуск приложения

   ```shell
   # Если используется poetry
   poetry shell
   poetry install                 
   # Если используется pip
   python -m venv venv
   ./venv/Scripts/activate
   pip install -r requirements.txt
   
   # Установка переменных окружения, необходимых для запуска приложения
   # Windows (PowerShell)
   $env:PYTHONPATH='src/'
   $env:FLASK_APP='src/runner.py'
   # Unix
   export PYTHONPATH='src/'
   export FLASK_APP='src/runner.py'
   
   # Запуск скрипта для создания БД
   python3 ./src/app/database/cli.py <create/drop/fill>
   # create - создание БД
   # drop - удаление БД
   # fill - заполнение БД тестовыми данными
   
   # Запуск приложения
   flask --app src/runner.py run
   ```