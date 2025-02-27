from django.contrib import admin
from .models import Route, Trip  # Импорт моделей

class RouteAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_point', 'end_point', 'created_at', 'updated_at')
    search_fields = ('name', 'start_point', 'end_point')

class TripAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'route', 'departure_time', 'arrival_time', 'created_at')
    search_fields = ('vehicle__vehicle_number', 'route__name')
    list_filter = ('departure_time', 'arrival_time')

# Регистрация моделей
admin.site.register(Route, RouteAdmin)
admin.site.register(Trip, TripAdmin)
