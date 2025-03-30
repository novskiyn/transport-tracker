from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .models import Client, ClientReview
from tracking.models import VehicleType, CompanyReview
from .serializers import ClientSerializer, ClientReviewSerializer
from rest_framework.permissions import IsAuthenticated
from authentication.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import ClientProfileForm, AvatarUpdateForm, CompanyReviewForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
            client = profile_form.save(commit=False)  # Получаем объект, но не сохраняем его

            # Обновляем данные пользователя
            user = client.user
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.save()  # Сохраняем обновленные данные пользователя

            client.save()  # Сохраняем профиль клиента

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


class CompanyReviewPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

@login_required
def reviews_page_client(request, user_id):
    # Получаем клиента на основе текущего пользователя
    client = get_object_or_404(Client, user__id=user_id)  # Одним запросом получаем клиента

    # Проверяем разрешения для клиента
    redirect_response = check_client_permission(request, client)
    if redirect_response:
        return redirect_response

    # Получаем все отзывы о компании
    company_reviews = CompanyReview.objects.all()

    # Проверка, есть ли уже отзыв у текущего пользователя
    existing_review = CompanyReview.objects.filter(user=request.user).first()

    # Пагинация
    paginator = Paginator(company_reviews, 5)  #  - количество отзывов на странице
    page = request.GET.get('page')

    try:
        result_page = paginator.page(page)
    except PageNotAnInteger:
        result_page = paginator.page(1)
    except EmptyPage:
        result_page = paginator.page(paginator.num_pages)

    # Обработка формы для добавления/редактирования отзыва
    if request.method == 'POST':
        if existing_review:  # Если отзыв уже существует, то редактируем его
            review_form = CompanyReviewForm(request.POST, instance=existing_review)
        else:  # Если отзыва нет, то создаем новый
            review_form = CompanyReviewForm(request.POST)
        
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user  # Связываем отзыв с текущим пользователем
            review.save()
            messages.success(request, "Ваш отзыв успешно сохранен!")
            return redirect('reviews_page_client', user_id=user_id)
    else:
        # Если отзыв уже существует, загружаем его в форму для редактирования
        if existing_review:
            review_form = CompanyReviewForm(instance=existing_review)
        else:
            review_form = CompanyReviewForm()

    # Удаление отзыва
    if request.method == 'POST' and 'delete_review' in request.POST:
        if existing_review:
            existing_review.delete()
            messages.success(request, "Ваш отзыв был удален!")
            return redirect('reviews_page_client', user_id=user_id)

    return render(request, 'client/reviews_page_client.html', {
        'client': client,  # Передаем клиента в шаблон
        'reviews': result_page,  # Передаем отзывы с пагинацией в шаблон
        'review_form': review_form,  # Передаем форму для добавления/редактирования отзыва
        'existing_review': existing_review  # Передаем информацию о существующем отзыве
    })



