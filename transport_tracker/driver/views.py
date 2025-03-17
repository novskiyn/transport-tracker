from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from tracking.models import VehicleType
from .models import Driver, DriverReview
from .serializers import DriverSerializer, DriverReviewSerializer
from django.shortcuts import get_object_or_404, redirect, render
from authentication.models import User
from django.contrib.auth.decorators import login_required

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
@login_required
def reviews_page_driver(request, user_id):
    driver = get_object_or_404(Driver, user__id=user_id)  # Одним запросом получаем водителя
    reviews = ClientReview.objects.filter(driver=driver)  # Получаем все отзывы для водителя
    redirect_response = check_driver_permission(request, driver)
    if redirect_response:
        return redirect_response
    return render(request, 'driver/reviews_page_driver.html', {'driver': driver, 'reviews': reviews})

# Страница профиля водителя
@login_required
def profile_page_driver(request, user_id):
    driver = get_object_or_404(Driver, user__id=user_id)  # Одним запросом получаем водителя
    redirect_response = check_driver_permission(request, driver)
    if redirect_response:
        return redirect_response
    return render(request, 'driver/profile_page_driver.html', {'driver': driver})

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








