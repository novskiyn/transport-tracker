from django.shortcuts import render
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .models import Driver, DriverReview
from .serializers import DriverSerializer, DriverReviewSerializer

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


