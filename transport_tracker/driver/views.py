from django.shortcuts import render
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from tracking.models import VehicleType
from .models import Driver, DriverReview
from .serializers import DriverSerializer, DriverReviewSerializer
from django.shortcuts import get_object_or_404, redirect
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

@login_required
def home_page_driver(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Получаем пользователя по user_id
    driver = get_object_or_404(Driver, user=user)  # Получаем водителя, связанного с этим пользователем
    
    # Проверяем, что текущий пользователь совпадает с водителем
    if driver.user.id != request.user.id:
        # Перенаправляем на страницу, только если текущий пользователь не совпадает с водителем
        return redirect('home_page_driver', user_id=request.user.id)  # Используем request.user.id для предотвращения цикличности

    return render(request, 'driver/home_page_driver.html', {'driver': driver})

# Страница информации о водителе и транспорте
def about_page_driver(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Получаем пользователя по user_id
    driver = get_object_or_404(Driver, user=user)  # Получаем водителя, связанного с этим пользователем
    transport_info = VehicleType.objects.all()  # Получаем все типы транспортных средств
    return render(request, 'driver/about_page_driver.html', {'driver': driver, 'transport_info': transport_info})

# Страница контактов
def contact_page_driver(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Получаем пользователя по user_id
    driver = get_object_or_404(Driver, user=user)  # Получаем водителя, связанного с этим пользователем
    return render(request, 'driver/contact_page_driver.html', {'driver': driver})

# Страница отзывов
def reviews_page_driver(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Получаем пользователя по user_id
    driver = get_object_or_404(Driver, user=user)  # Получаем водителя, связанного с этим пользователем
    return render(request, 'driver/reviews_page_driver.html', {'driver': driver})

# Страница профиля водителя
def profile_page_driver(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Получаем пользователя по user_id
    driver = get_object_or_404(Driver, user=user)  # Получаем водителя, связанного с этим пользователем
    return render(request, 'driver/profile_page_driver.html', {'driver': driver})

# Страница карты
def map_page_driver(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Получаем пользователя по user_id
    driver = get_object_or_404(Driver, user=user)  # Получаем водителя, связанного с этим пользователем
    return render(request, 'driver/map_page_driver.html', {'driver': driver})

# История водителя
def history_page_driver(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Получаем пользователя по user_id
    driver = get_object_or_404(Driver, user=user)  # Получаем водителя, связанного с этим пользователем
    return render(request, 'driver/history_page_driver.html', {'driver': driver})









