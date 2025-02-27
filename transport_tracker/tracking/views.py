from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .models import Vehicle, Driver, DriverReview
from .serializers import VehicleSerializer, DriverSerializer, DriverReviewSerializer

class VehiclePagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

class DriverPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

class DriverReviewPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['status', 'driver']
    ordering_fields = ['vehicle_number', 'last_updated']
    ordering = ['last_updated']
    pagination_class = VehiclePagination
    permission_classes = [IsAuthenticated]

class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['first_name', 'last_name', 'rating']
    ordering_fields = ['first_name', 'last_name', 'rating']
    ordering = ['last_name']
    pagination_class = DriverPagination
    permission_classes = [IsAuthenticated]

class DriverReviewViewSet(viewsets.ModelViewSet):
    queryset = DriverReview.objects.all()
    serializer_class = DriverReviewSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['driver', 'user', 'rating']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']
    pagination_class = DriverReviewPagination
    permission_classes = [IsAuthenticated]
