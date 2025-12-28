#!/bin/bash
# docker-entrypoint.sh

# Ждем, пока всё инициализируется
echo "🚀 Запуск Django приложения в Docker..."

# Применяем миграции
echo "📦 Применяем миграции..."
python manage.py migrate

# Собираем статику (уже в Dockerfile, но на всякий случай)
echo "🎨 Собираем статику..."
python manage.py collectstatic --noinput

# Создаем суперпользователя, если его нет
echo "👑 Проверяем суперпользователя..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✅ Суперпользователь создан')
else:
    print('✅ Суперпользователь уже существует')
"

# Запускаем Gunicorn
echo "🏃 Запускаем сервер..."
exec gunicorn --bind 0.0.0.0:8000 djangoProject.wsgi:application