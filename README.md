
﻿my-django-project
=======

Стек технологий
-----------------------------------------------------------------------------------------------------------
Backend: Python 3.10+, Django 4.2, Django REST Framework

База данных: PostgreSQL / SQLite

Инфраструктура: Docker, Docker Compose, Gunicorn

Frontend: Bootstrap 5, HTML/CSS, JavaScript

Установка и запуск
-----------------------------------------------------------------------------------------------------------
Локальная разработка (без Docker)
cd user-management

python -m venv venv

source venv/bin/activate # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env

Отредактируйте .env файл
python manage.py migrate

python manage.py createsuperuser

python manage.py runserver

Запуск с Docker
-----------------------------------------------------------------------------------------------------------
bash docker-compose up --build

Основные функции
-----------------------------------------------------------------------------------------------------------
CRUD операции для пользователей

Поиск и фильтрация пользователей

Пагинация списков

Валидация данных (email, телефон, пароль)

REST API для интеграций

Docker-контейнеризация

API Endpoints



GET /api/v1/users/ - список пользователей

POST /api/v1/users/ - создать пользователя

GET /api/v1/users/{id}/ - детали пользователя

PUT /api/v1/users/{id}/ - обновить пользователя

DELETE /api/v1/users/{id}/ - удалить пользователя

Структура проекта
-----------------------------------------------------------------------------------------------------------
text

user_management/

├── src/

│ ├── users/ - приложение управления пользователями

│ ├── config/ - конфигурация проекта

│ ├── api/ - REST API приложение

│ └── static/ - статические файлы

├── docker/ - Docker конфигурации

├── tests/ - модульные тесты

├── docker-compose.yml

├── Dockerfile

├── requirements.txt

└── manage.py

Переменные окружения (.env)

text

DEBUG=True

SECRET_KEY=*********

ALLOWED_HOSTS=localhost,127.0.0.1

DB_ENGINE=django.db.backends.postgresql

DB_NAME=user_db

DB_USER=user_admin

DB_PASSWORD=secure_password

DB_HOST=db

DB_PORT=5432

Автор
-----------------------------------------------------------------------------------------------------------
Прохорович Тимофей Михайлович

GitHub: nbnpro123

Email: prohorovict39@gmail.com

Для рекрутеров
-----------------------------------------------------------------------------------------------------------
Этот проект демонстрирует навыки:

Backend разработка: Django, DRF, PostgreSQL

Инфраструктура: Docker, Docker Compose

Frontend основы: Bootstrap

Архитектура: чистый код, REST API

Документация: подробная документация установки

Проект готов к деплою на любой VPS и может служить основой для реальных систем управления пользователями.
<<<<<<< HEAD
=======


>>>>>>> 5f5fc63ce4aa321a49222e762e066981e00086c4

