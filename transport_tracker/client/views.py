from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .models import Client, ClientReview
from tracking.models import VehicleType
from .serializers import ClientSerializer, ClientReviewSerializer
from rest_framework.permissions import IsAuthenticated
from authentication.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import ClientProfileForm, AvatarUpdateForm
from django.contrib import messages


# Пагинация для клиентов
class ClientPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

# Пагинация для отзывов клиентов
class ClientReviewPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

# ViewSet для клиентов
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['first_name', 'last_name', 'rating']
    ordering_fields = ['first_name', 'last_name', 'rating']
    ordering = ['last_name']
    pagination_class = ClientPagination
    permission_classes = [IsAuthenticated]

# ViewSet для отзывов клиентов
class ClientReviewViewSet(viewsets.ModelViewSet):
    queryset = ClientReview.objects.all()
    serializer_class = ClientReviewSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['client', 'driver', 'rating']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']
    pagination_class = ClientReviewPagination
    permission_classes = [IsAuthenticated]

# Универсальная функция для проверки разрешений
def check_client_permission(request, client):
    if client.user != request.user:
        # Перенаправляем на страницу клиента с текущим пользователем
        return redirect('home_page_client', user_id=request.user.id)
    return None  # Если все в порядке, возвращаем None

# Представление домашней страницы клиента
@login_required
def home_page_client(request, user_id):
    client = get_object_or_404(Client, user__id=user_id)  # Одним запросом получаем клиента
    redirect_response = check_client_permission(request, client)
    if redirect_response:
        return redirect_response
    return render(request, 'client/home_page_client.html', {'client': client})

# Представление страницы "О компании" для клиента
@login_required
def about_page_client(request, user_id):
    client = get_object_or_404(Client, user__id=user_id)  # Одним запросом получаем клиента
    transport_info = VehicleType.objects.all()  # Получаем все типы транспортных средств
    redirect_response = check_client_permission(request, client)
    if redirect_response:
        return redirect_response
    return render(request, 'client/about_page_client.html', {'client': client, 'transport_info': transport_info})

# Представление страницы "Контакты" для клиента
@login_required
def contact_page_client(request, user_id):
    client = get_object_or_404(Client, user__id=user_id)  # Одним запросом получаем клиента
    redirect_response = check_client_permission(request, client)
    if redirect_response:
        return redirect_response
    return render(request, 'client/contact_page_client.html', {'client': client})

# Представление страницы отзывов клиента
@login_required
def reviews_page_client(request, user_id):
    client = get_object_or_404(Client, user__id=user_id)  # Одним запросом получаем клиента
    reviews = ClientReview.objects.filter(client=client)  # Получаем все отзывы для клиента
    redirect_response = check_client_permission(request, client)
    if redirect_response:
        return redirect_response
    return render(request, 'client/reviews_page_client.html', {'client': client, 'reviews': reviews})

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required
def profile_page_client(request, user_id):
    client = get_object_or_404(Client, user__id=user_id)

    if request.method == 'POST':
        # Обработка удаления аватара
        if 'delete_avatar' in request.POST:
            client.avatar.delete()  # Удаляем аватар
            messages.success(request, "Аватар удален!")
            return redirect('profile_page_client', user_id=user_id)

        # Обработка обновления профиля
        profile_form = ClientProfileForm(request.POST, instance=client)
        avatar_form = AvatarUpdateForm(request.POST, request.FILES, instance=client)

        if profile_form.is_valid():
            profile_form.save()

        if avatar_form.is_valid():
            avatar_form.save()

        # Обработка смены пароля
        if 'change_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Обновление сессии после смены пароля
                messages.success(request, "Пароль изменен успешно!")
                return redirect('profile_page_client', user_id=user_id)
            else:
                messages.error(request, "Ошибка при смене пароля.")
        else:
            password_form = PasswordChangeForm(request.user)

        messages.success(request, "Данные профиля обновлены!")
        return redirect('profile_page_client', user_id=user_id)

    # Передаем форму смены пароля в контекст
    profile_form = ClientProfileForm(instance=client)
    avatar_form = AvatarUpdateForm(instance=client)
    password_form = PasswordChangeForm(request.user)

    return render(request, 'client/profile_page_client.html', {
        'client': client,
        'profile_form': profile_form,
        'avatar_form': avatar_form,
        'password_form': password_form,  # Передаем форму смены пароля
    })


# Представление страницы карты клиента
@login_required
def map_page_client(request, user_id):
    client = get_object_or_404(Client, user__id=user_id)  # Одним запросом получаем клиента
    redirect_response = check_client_permission(request, client)
    if redirect_response:
        return redirect_response
    return render(request, 'client/map_page_client.html', {'client': client})

# Представление страницы истории клиента
@login_required
def history_page_client(request, user_id):
    client = get_object_or_404(Client, user__id=user_id)  # Одним запросом получаем клиента
    redirect_response = check_client_permission(request, client)
    if redirect_response:
        return redirect_response
    return render(request, 'client/history_page_client.html', {'client': client})

def logout_user(request):
    logout(request)  # Выход из системы
    return redirect('login_page')    

