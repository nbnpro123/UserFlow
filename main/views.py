from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import Http404
import json
import os
from datetime import datetime


# Функция для получения пути к файлу данных
def get_data_file_path():
    # Получаем базовую директорию проекта
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')

    # Создаем папку data, если она не существует
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    return os.path.join(data_dir, 'users.json')


# Функция для загрузки пользователей из файла
def load_users():
    file_path = get_data_file_path()

    # Если файл не существует, создаем его с пустым списком
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump([], file, ensure_ascii=False, indent=2)
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            users = json.load(file)

            # Преобразуем строки created_at в объекты datetime
            for user in users:
                if 'created_at' in user and isinstance(user['created_at'], str):
                    try:
                        date_str = user['created_at'].split('.')[0]  # Убираем микросекунды
                        user['created_at'] = datetime.fromisoformat(date_str)
                    except (ValueError, AttributeError):
                        # Если не получается преобразовать, оставляем строку
                        pass
            return users
    except (json.JSONDecodeError, FileNotFoundError):
        return []


# Функция для сохранения пользователей в файл
def save_users(users):
    file_path = get_data_file_path()

    # Убедимся, что папка существует
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Преобразуем datetime обратно в строку
    users_to_save = []
    for user in users:
        user_copy = user.copy()

        if 'created_at' in user_copy and isinstance(user_copy['created_at'], datetime):
            user_copy['created_at'] = user_copy['created_at'].isoformat()

        users_to_save.append(user_copy)

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(users_to_save, file, ensure_ascii=False, indent=2)


def main(request):
    """Главная страница"""
    return render(request, 'main/list.html')


def main_list(request):
    """Панель действий"""
    return render(request, 'main/main_list.html')


def list_users(request):
    """Показать список всех пользователей"""
    users = load_users()

    # Рассчитываем статистику
    total_users = len(users)
    average_age = 0
    min_age = None
    max_age = None

    if users:
        ages = [user.get('age', 0) for user in users if user.get('age') is not None]

        if ages:
            total_age = sum(ages)
            average_age = total_age / len(ages)
            min_age = min(ages)
            max_age = max(ages)

    return render(request, 'main/list_users.html', {
        'users': users,
        'total_users': total_users,
        'average_age': round(average_age, 1) if average_age else 0,
        'min_age': min_age,
        'max_age': max_age
    })


def register_view(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        # Получаем данные из формы
        name = request.POST.get('name', '').strip()
        age = request.POST.get('age', '').strip()
        email = request.POST.get('email', '').strip()

        # Валидация
        if not name or not age or not email:
            messages.error(request, 'Все поля обязательны для заполнения!')
            return render(request, 'main/register.html')

        try:
            age = int(age)
            if age <= 0 or age > 150:
                messages.error(request, 'Возраст должен быть от 1 до 150 лет!')
                return render(request, 'main/register.html')
        except ValueError:
            messages.error(request, 'Возраст должен быть числом!')
            return render(request, 'main/register.html')

        # Загружаем существующих пользователей
        users = load_users()

        # Генерируем ID (максимальный существующий ID + 1)
        max_id = max([user.get('id', 0) for user in users], default=0)

        # Создаем нового пользователя
        new_user = {
            'id': max_id + 1,
            'name': name,
            'age': age,
            'email': email,
            'created_at': datetime.now()
        }

        # Добавляем пользователя и сохраняем
        users.append(new_user)
        save_users(users)

        messages.success(request, f'✅ Пользователь "{name}" успешно добавлен!')
        return redirect('list_users')

    return render(request, 'main/register.html')


def user_detail(request, user_id):
    """Показать детальную информацию о пользователе"""
    users = load_users()

    # Ищем пользователя по ID
    user = None
    for u in users:
        if u.get('id') == int(user_id):
            user = u
            break

    if not user:
        raise Http404("Пользователь не найден")

    return render(request, 'main/user_detail.html', {'user': user})