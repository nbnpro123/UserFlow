from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Avg, Max, Min, Sum
from .models import User
from django.db.models import Q



def main(request):
    return render(request, 'main/list.html')


def main_list(request):
    return render(request, 'main/main_list.html')


def list_users(request):
    search_query = request.GET.get('search', '')
    users = User.objects.all()
    if search_query:
        users = users.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(age__icontains=search_query)
        )

    total_users = users.count()

    if total_users > 0:
        average_age = users.aggregate(Avg('age'))['age__avg']
        max_age = users.aggregate(Max('age'))['age__max']
    else:
        average_age = 0
        max_age = None

    context = {
        'users': users,
        'total_users': total_users,
        'average_age': average_age,
        'max_age': max_age,
        'search_query': search_query,
    }

    return render(request, 'main/list_users.html', context)


def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        age = request.POST.get('age', '').strip()
        email = request.POST.get('email', '').strip()

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


        if User.objects.filter(email=email).exclude(id=user_id).exists():
            messages.error(request, 'Пользователь с таким email уже существует!')
            return render(request, 'main/edit_user.html', {'user': user})


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


    return render(request, 'main/edit_user.html', {'user': user})


def register_view(request):

    if request.method == 'POST':

        name = request.POST.get('name', '').strip()
        age = request.POST.get('age', '').strip()
        email = request.POST.get('email', '').strip()


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


        try:
            User.objects.create(
                name=name,
                age=age,
                email=email
            )
            messages.success(request, f'✅ Пользователь "{name}" успешно добавлен!')
            return redirect('list_users')

        except Exception as e:

            error_message = str(e)
            if 'UNIQUE constraint' in error_message or 'unique' in error_message.lower():
                messages.error(request, 'Пользователь с таким email уже существует!')
            else:
                messages.error(request, f'Ошибка при создании пользователя: {error_message}')
            return render(request, 'main/register.html')


    return render(request, 'main/register.html')


def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)


    if user.created_at:
        from django.utils import timezone
        time_in_system = timezone.now() - user.created_at
        time_in_system_display = time_in_system.days
    else:
        time_in_system_display = 0

    context = {
        'user': user,
        'time_in_system': time_in_system_display,
    }

    return render(request, 'main/user_detail.html', context)


def delete_user(request, user_id):

    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':

        user_name = user.name


        user.delete()

        messages.success(request, f'✅ Пользователь "{user_name}" успешно удален!')
        return redirect('list_users')

    return render(request, 'main/user_confirm_delete.html', {'user': user})