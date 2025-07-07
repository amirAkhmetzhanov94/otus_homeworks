# 📝 Django Blog — OTUS Homework
Блог-приложение, разработанное в рамках домашнего задания OTUS. Реализован на Django 5.2 с применением продакшен-практик и принципов 12-Factor App.

## 🚀 Функциональность
* Отображение списка постов
* Детальная страница поста
* Комментарии
* Классические Django Views + HTML-шаблоны
* Админка
* Логгирование в файл
* Настройки через `.env`
* Поддержка Docker, Makefile и Poetry

## ⚙️ Запуск через Docker
1. Клонируйте проект:
   ```bash
   git clone <репозиторий>
   cd <папка>
   ```

2. Создайте файл `.env`:
   ```env
   SECRET_KEY=your_secret_key
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost
   TIME_ZONE=Asia/Almaty
   LANGUAGE_CODE=ru
   POSTGRES_DB=blog
   POSTGRES_USER=blog_user
   POSTGRES_PASSWORD=blog_pass
   DB_NAME=blog
   DB_USER=blog_user
   DB_PASSWORD=blog_pass
   DB_HOST=db
   DB_PORT=5432
   ```

3. Поднимите проект:
   ```bash
   make build
   make up
   ```

4. Примените миграции и создайте суперпользователя:
   ```bash
   make migrate
   make createsuperuser
   ```

## 🧪 Тесты
```bash
pytest
```

## 📂 Структура проекта
* `blog/` — приложение с моделями, views и шаблонами
* `otus_homework_django/` — настройки Django
* `templates/` — HTML-шаблоны
* `entrypoint.sh`, `Dockerfile`, `docker-compose.yml`, `Makefile` — DevOps-инфраструктура
* `.env` — конфигурация
* `debug.log` — лог-файл
* `requirements.txt`, `pyproject.toml`, `poetry.lock` — зависимости

## 📌 Особенности
* Все настройки конфигурации вынесены в `.env`
* Поддержка сборки через Poetry (`--no-root`)
* WhiteNoise подключен для отдачи статики
* Makefile ускоряет команды запуска/сбора