from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from tracking.models import VehicleType, CompanyReview
from .models import Driver, DriverReview
from .serializers import DriverSerializer, DriverReviewSerializer
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from authentication.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import DriverProfileForm, AvatarUpdateForm, CompanyReviewForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Пагинация для водителей
class DriverPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

# Пагинация для отзывов водителей
class DriverReviewPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

# ViewSet для водителей
class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['first_name', 'last_name', 'rating']
    ordering_fields = ['first_name', 'last_name', 'rating']
    ordering = ['last_name']
    pagination_class = DriverPagination
    permission_classes = [IsAuthenticated]

# ViewSet для отзывов водителей
class DriverReviewViewSet(viewsets.ModelViewSet):
    queryset = DriverReview.objects.all()
    serializer_class = DriverReviewSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['driver', 'user', 'rating']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']
    pagination_class = DriverReviewPagination
    permission_classes = [IsAuthenticated]


# Универсальная функция для проверки разрешений
def check_driver_permission(request, driver):
    if driver.user != request.user:
        # Перенаправляем на страницу водителя с текущим пользователем
        return redirect('home_page_driver', user_id=request.user.id)
    return None  # Если все в порядке, возвращаем None

# Представление домашней страницы водителя
@login_required
def home_page_driver(request, user_id):
    driver = get_object_or_404(Driver, user__id=user_id)  # Одним запросом получаем водителя
    redirect_response = check_driver_permission(request, driver)
    if redirect_response:
        return redirect_response
    return render(request, 'driver/home_page_driver.html', {'driver': driver})

# Страница информации о водителе и транспорте
@login_required
def about_page_driver(request, user_id):
    driver = get_object_or_404(Driver, user__id=user_id)  # Одним запросом получаем водителя
    transport_info = VehicleType.objects.all()  # Получаем все типы транспортных средств
    redirect_response = check_driver_permission(request, driver)
    if redirect_response:
        return redirect_response
    return render(request, 'driver/about_page_driver.html', {'driver': driver, 'transport_info': transport_info})

# Страница контактов водителя
@login_required
def contact_page_driver(request, user_id):
    driver = get_object_or_404(Driver, user__id=user_id)  # Одним запросом получаем водителя
    redirect_response = check_driver_permission(request, driver)
    if redirect_response:
        return redirect_response
    return render(request, 'driver/contact_page_driver.html', {'driver': driver})

# Страница отзывов для водителя
class CompanyReviewPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

@login_required
def reviews_page_driver(request, user_id):
    # Получаем клиента на основе текущего пользователя
    driver = get_object_or_404(Driver, user__id=user_id)  # Одним запросом получаем клиента

    # Проверяем разрешения для клиента
    redirect_response = check_driver_permission(request, driver)
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
            return redirect('reviews_page_driver', user_id=user_id)
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
            return redirect('reviews_page_driver', user_id=user_id)

    return render(request, 'driver/reviews_page_driver.html', {
        'driver': driver,  # Передаем клиента в шаблон
        'reviews': result_page,  # Передаем отзывы с пагинацией в шаблон
        'review_form': review_form,  # Передаем форму для добавления/редактирования отзыва
        'existing_review': existing_review  # Передаем информацию о существующем отзыве
    })

# Страница профиля водителя
@login_required
def profile_page_driver(request, user_id):
    # Получаем объект водителя по user_id
    driver = get_object_or_404(Driver, user__id=user_id)

    if request.method == 'POST':
        # Обработка удаления аватара
        if 'delete_avatar' in request.POST:
            driver.avatar.delete()  # Удаляем аватар
            messages.success(request, "Аватар удален!")
            return redirect('profile_page_driver', user_id=user_id)

        # Обработка обновления профиля водителя
        profile_form = DriverProfileForm(request.POST, instance=driver)
        avatar_form = AvatarUpdateForm(request.POST, request.FILES, instance=driver)

        if profile_form.is_valid():
            driver = profile_form.save(commit=False)  # Получаем объект, но не сохраняем его

            # Обновляем данные пользователя
            user = driver.user
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.save()  # Сохраняем обновленные данные пользователя

            driver.save()  # Сохраняем профиль водителя

        if avatar_form.is_valid():
            avatar_form.save()  # Сохраняем аватар

        # Обработка смены пароля
        if 'change_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Обновление сессии после смены пароля
                messages.success(request, "Пароль изменен успешно!")
                return redirect('profile_page_driver', user_id=user_id)
            else:
                messages.error(request, "Ошибка при смене пароля.")
        else:
            password_form = PasswordChangeForm(request.user)

        messages.success(request, "Данные профиля обновлены!")
        return redirect('profile_page_driver', user_id=user_id)

    # Передаем форму смены пароля в контекст
    profile_form = DriverProfileForm(instance=driver)
    avatar_form = AvatarUpdateForm(instance=driver)
    password_form = PasswordChangeForm(request.user)

    return render(request, 'driver/profile_page_driver.html', {
        'driver': driver,
        'profile_form': profile_form,
        'avatar_form': avatar_form,
        'password_form': password_form,  # Передаем форму смены пароля
    })

# Страница карты для водителя
@login_required
def map_page_driver(request, user_id):
    driver = get_object_or_404(Driver, user__id=user_id)  # Одним запросом получаем водителя
    redirect_response = check_driver_permission(request, driver)
    if redirect_response:
        return redirect_response
    return render(request, 'driver/map_page_driver.html', {'driver': driver})

# Страница истории для водителя
@login_required
def history_page_driver(request, user_id):
    driver = get_object_or_404(Driver, user__id=user_id)  # Одним запросом получаем водителя
    redirect_response = check_driver_permission(request, driver)
    if redirect_response:
        return redirect_response
    return render(request, 'driver/history_page_driver.html', {'driver': driver})

def logout_user(request):
    logout(request)  # Выход из системы
    return redirect('login_page')  








