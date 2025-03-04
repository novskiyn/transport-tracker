from django.shortcuts import render
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .models import Route, Trip
from tracking.models import VehicleType
from .serializers import RouteSerializer, TripSerializer

def home_page(request):
    return render(request, 'user/home_page.html')  

def about_page(request):
    transport_info = VehicleType.objects.all()
    return render(request, 'user/about_page.html', {'transport_info': transport_info})   

def contact_page(request):
    return render(request, 'user/contact_page.html')  

class RoutePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class TripPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['name', 'start_point', 'end_point']
    ordering_fields = ['name', 'created_at']
    ordering = ['created_at']
    pagination_class = RoutePagination
    permission_classes = [IsAuthenticated]

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['vehicle', 'route', 'departure_time', 'arrival_time']
    ordering_fields = ['departure_time', 'arrival_time']
    ordering = ['departure_time']
    pagination_class = TripPagination
    permission_classes = [IsAuthenticated]
