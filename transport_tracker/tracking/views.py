from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .models import Vehicle, Driver, DriverReview, VehicleType
from .serializers import VehicleSerializer, DriverSerializer, DriverReviewSerializer, VehicleTypeSerializer

# Пагинация для транспортных средств
class VehiclePagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

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

# ViewSet для транспортных средств
class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['status', 'driver', 'vehicle_type']  # Фильтрация по статусу, водителю и типу транспорта
    ordering_fields = ['vehicle_number', 'vehicle_type__name']  # Убираем last_updated из сортировки
    ordering = ['vehicle_number']  # Пример сортировки по номеру
    pagination_class = VehiclePagination
    permission_classes = [IsAuthenticated]


# ViewSet для водителей
class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['first_name', 'last_name', 'rating']  # Фильтрация по имени, фамилии и рейтингу
    ordering_fields = ['first_name', 'last_name', 'rating']  # Сортировка по этим же полям
    ordering = ['last_name']
    pagination_class = DriverPagination
    permission_classes = [IsAuthenticated]

# ViewSet для отзывов водителей  
class DriverReviewViewSet(viewsets.ModelViewSet):
    queryset = DriverReview.objects.all()
    serializer_class = DriverReviewSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['driver', 'user', 'rating']  # Фильтрация по водителю, пользователю и рейтингу
    ordering_fields = ['created_at', 'rating']  # Сортировка по дате создания и рейтингу
    ordering = ['-created_at']
    pagination_class = DriverReviewPagination
    permission_classes = [IsAuthenticated]

# ViewSet для типов транспорта
class VehicleTypeViewSet(viewsets.ModelViewSet):
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer  # Исправлено на правильный сериализатор
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['name']  # Фильтрация по имени типа транспорта
    ordering_fields = ['name', 'brand']  # Сортировка по имени и бренду
    ordering = ['name']
    permission_classes = [IsAuthenticated]
