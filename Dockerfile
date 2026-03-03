# Dockerfile
FROM python:3.11-alpine

# Устанавливаем системные зависимости для сборки Python пакетов
RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    postgresql-dev \
    && rm -rf /var/cache/apk/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Сначала копируем requirements.txt для кэширования
COPY requirements.txt .

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Теперь копируем остальной код
COPY . .

# Создаем необходимые папки
RUN mkdir -p /app/data /app/static /app/media

# Меняем владельца (для безопасности)
RUN adduser -D appuser && chown -R appuser:appuser /app
USER appuser

# Собираем статику
RUN python manage.py collectstatic --noinput

# Открываем порт
EXPOSE 8000

# Команда запуска
CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 --workers 3 djangoProject.wsgi:application"]