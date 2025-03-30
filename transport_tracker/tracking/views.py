from django.shortcuts import render
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .models import Vehicle, VehicleType, Route, Trip, CompanyReview
from .serializers import VehicleSerializer, VehicleTypeSerializer, RouteSerializer, TripSerializer, CompanyReviewSerializer

# Пагинация для транспортных средств
class VehiclePagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

# Пагинация для маршрутов
class RoutePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# Пагинация для поездок
class TripPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50

# ViewSet для транспортных средств
class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['status', 'driver', 'vehicle_type']
    ordering_fields = ['vehicle_number', 'vehicle_type__name']
    ordering = ['vehicle_number']
    pagination_class = VehiclePagination
    permission_classes = [IsAuthenticated]

# ViewSet для типов транспорта
class VehicleTypeViewSet(viewsets.ModelViewSet):
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['name']
    ordering_fields = ['name', 'brand']
    ordering = ['name']
    permission_classes = [IsAuthenticated]

# ViewSet для маршрутов
class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['name', 'start_point', 'end_point']
    ordering_fields = ['name', 'created_at']
    ordering = ['created_at']
    pagination_class = RoutePagination
    permission_classes = [IsAuthenticated]

# ViewSet для поездок
class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['vehicle', 'route', 'departure_time', 'arrival_time']
    ordering_fields = ['departure_time', 'arrival_time']
    ordering = ['departure_time']
    pagination_class = TripPagination
    permission_classes = [IsAuthenticated]

class CompanyReviewViewSet(viewsets.ModelViewSet):
    queryset = CompanyReview.objects.all()
    serializer_class = CompanyReviewSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['user', 'rating']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']
    permission_classes = [IsAuthenticated]