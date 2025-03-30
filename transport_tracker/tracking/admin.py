from django.contrib import admin
from .models import Vehicle, VehicleType, Route, Trip, CompanyReview  # Импорт всех моделей

# Админ-классы для транспортных средств
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        'vehicle_number', 
        'current_location', 
        'status', 
        'driver', 
        'vehicle_type', 
    )
    search_fields = ('vehicle_number', 'driver__first_name', 'driver__last_name', 'vehicle_type__name')  # Поиск по типу транспорта
    list_filter = ('status', 'vehicle_type')  # Фильтрация по типу транспорта

class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'max_capacity', 'year_of_manufacture', 'description')  # Показываем характеристики типа транспорта
    search_fields = ('name', 'brand', 'description')  # Поиск по имени типа, бренду и описанию

# Админ-классы для маршрутов и поездок
class RouteAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_point', 'end_point', 'created_at', 'updated_at')
    search_fields = ('name', 'start_point', 'end_point')

class TripAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'route', 'departure_time', 'arrival_time', 'created_at')
    search_fields = ('vehicle__vehicle_number', 'route__name')
    list_filter = ('departure_time', 'arrival_time')

# Админ-класс для отзывов о компании
class CompanyReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'created_at')  # Показываем пользователя, рейтинг и дату создания
    search_fields = ('user__username', 'rating')  # Поиск по имени пользователя и рейтингу
    list_filter = ('rating',)  # Фильтрация по рейтингу
    date_hierarchy = 'created_at'  # Дата для иерархической фильтрации

# Регистрация моделей в админке
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(VehicleType, VehicleTypeAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(Trip, TripAdmin)
admin.site.register(CompanyReview, CompanyReviewAdmin)  # Регистрация модели отзывов
