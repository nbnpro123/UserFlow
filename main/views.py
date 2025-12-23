from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Avg, Max, Min, Sum
from .models import User


def main(request):
    """Главная страница"""
    return render(request, 'main/list.html')


def main_list(request):
    """Панель действий"""
    return render(request, 'main/main_list.html')


def list_users(request):
    """Показать список всех пользователей"""
    # Получаем всех пользователей из базы данных
    users = User.objects.all().order_by('-created_at')

    # Рассчитываем статистику через агрегацию (быстрее и эффективнее)
    total_users = users.count()

    if total_users > 0:
        # Используем агрегатные функции Django для вычислений
        stats = users.aggregate(
            average_age=Avg('age'),
            min_age=Min('age'),
            max_age=Max('age')
        )

        average_age = stats['average_age'] or 0
        min_age = stats['min_age']
        max_age = stats['max_age']
    else:
        average_age = min_age = max_age = 0

    return render(request, 'main/list_users.html', {
        'users': users,
        'total_users': total_users,
        'average_age': round(average_age, 1),
        'min_age': min_age,
        'max_age': max_age
    })


def edit_user(request, user_id):
    """Редактирование пользователя"""
    # Получаем пользователя или возвращаем 404
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        # Получаем данные из формы
        name = request.POST.get('name', '').strip()
        age = request.POST.get('age', '').strip()
        email = request.POST.get('email', '').strip()

        # Валидация
        if not name or not age or not email:
            messages.error(request, 'Все поля обязательны для заполнения!')
            return render(request, 'main/edit_user.html', {'user': user})

        try:
            age = int(age)
            if age <= 0 or age > 150:
                messages.error(request, 'Возраст должен быть от 1 до 150 лет!')
                return render(request, 'main/edit_user.html', {'user': user})
        except ValueError:
            messages.error(request, 'Возраст должен быть числом!')
            return render(request, 'main/edit_user.html', {'user': user})

        # Проверяем, не занят ли email другим пользователем (кроме текущего)
        if User.objects.filter(email=email).exclude(id=user_id).exists():
            messages.error(request, 'Пользователь с таким email уже существует!')
            return render(request, 'main/edit_user.html', {'user': user})

        # Обновляем данные пользователя
        try:
            user.name = name
            user.age = age
            user.email = email
            user.save()

            messages.success(request, f'✅ Данные пользователя "{name}" успешно обновлены!')
            return redirect('list_users')
        except Exception as e:
            messages.error(request, f'Ошибка при обновлении: {str(e)}')
            return render(request, 'main/edit_user.html', {'user': user})

    # Если GET запрос - показываем форму редактирования
    return render(request, 'main/edit_user.html', {'user': user})


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

        # Создаем нового пользователя в базе данных
        try:
            User.objects.create(
                name=name,
                age=age,
                email=email
            )
            messages.success(request, f'✅ Пользователь "{name}" успешно добавлен!')
            return redirect('list_users')

        except Exception as e:
            # Обработка ошибок (например, если email уже существует)
            error_message = str(e)
            if 'UNIQUE constraint' in error_message or 'unique' in error_message.lower():
                messages.error(request, 'Пользователь с таким email уже существует!')
            else:
                messages.error(request, f'Ошибка при создании пользователя: {error_message}')
            return render(request, 'main/register.html')

    # Если GET запрос - просто показываем форму
    return render(request, 'main/register.html')


def user_detail(request, user_id):
    """Показать детальную информацию о пользователе"""
    # Используем get_object_or_404 для автоматической обработки 404 ошибки
    user = get_object_or_404(User, id=user_id)
    return render(request, 'main/user_detail.html', {'user': user})


def delete_user(request, user_id):
    """Удаление пользователя"""
    # Находим пользователя или возвращаем 404
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        # Сохраняем имя для сообщения об успехе
        user_name = user.name

        # Удаляем пользователя из базы данных
        user.delete()

        messages.success(request, f'✅ Пользователь "{user_name}" успешно удален!')
        return redirect('list_users')

    # Если GET запрос - показываем страницу подтверждения
    return render(request, 'main/user_confirm_delete.html', {'user': user})