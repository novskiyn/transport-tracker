from django.db import models
from django.apps import apps
from django.conf import settings
from authentication.models import User
from driver.models import Driver

# Модели для маршрутов и поездок (Map App)
class Route(models.Model):
    name = models.CharField(max_length=100)
    start_point = models.CharField(max_length=255)
    end_point = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class CompanyReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="company_reviews")  # Используем AUTH_USER_MODEL
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])  # Рейтинг от 1 до 5
    review_text = models.TextField(blank=True, null=True)  # Текст отзыва
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания
    
    class Meta:
        ordering = ['-created_at']  # Последние отзывы первыми
    
    def __str__(self):
        return f"Отзыв {self.rating}⭐ от {self.user.username}"


class Trip(models.Model):
    vehicle = models.ForeignKey('Vehicle', related_name='trips', on_delete=models.CASCADE)  # Ленивая загрузка
    route = models.ForeignKey(Route, related_name='trips', on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vehicle} по маршруту {self.route} с {self.departure_time} до {self.arrival_time}"


class VehicleType(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Название типа транспорта (например, грузовик, автобус)
    brand = models.CharField(max_length=50, default='Unknown')  # Бренд типа транспорта
    max_capacity = models.PositiveIntegerField(null=True, blank=True)  # Максимальная грузоподъемность в килограммах
    year_of_manufacture = models.PositiveIntegerField(null=True, blank=True)  # Год выпуска типа транспорта
    description = models.TextField(blank=True, null=True)  # Описание типа транспорта
    image = models.ImageField(upload_to='vehicle_types/', null=True, blank=True)  # Изображение типа транспорта

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    vehicle_number = models.CharField(max_length=50)  # Номер транспортного средства
    current_location = models.CharField(max_length=255)  # Текущее местоположение
    status = models.CharField(max_length=20, choices=[  # Статус транспортного средства
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('on_route', 'On Route'),
    ])
    driver = models.OneToOneField(Driver, on_delete=models.CASCADE, related_name='vehicle', null=True)  # Водитель
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE, related_name='vehicles', null=True, blank=True)  # Тип транспорта, теперь можно быть пустым

    def __str__(self):
        return f'{self.vehicle_number} - {self.vehicle_type.name if self.vehicle_type else "Unknown"}'

    def get_routes(self):
        Route = apps.get_model('tracking', 'Route')  
        return Route.objects.filter(vehicles=self)
