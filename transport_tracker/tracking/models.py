from django.db import models
from django.apps import apps  
from map.models import Trip
from django.contrib.auth.models import User


class Driver(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=15)
    rating = models.FloatField(default=0)
    review_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def update_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            total_rating = sum(review.rating for review in reviews)
            self.rating = total_rating / reviews.count()
            self.review_count = reviews.count()
        else:
            self.rating = 0
            self.review_count = 0
        self.save()

    def can_take_trip(self, departure_time, arrival_time):
        trips = Trip.objects.filter(vehicle__driver=self)
        for trip in trips:
            if (departure_time < trip.arrival_time and arrival_time > trip.departure_time):
                return False
        return True    


class DriverReview(models.Model):
    driver = models.ForeignKey(Driver, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='driver_reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.driver.update_rating()

    def __str__(self):
        return f"Отзыв о {self.driver} от {self.user.username}: {self.rating} звезд"


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
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('on_route', 'On Route'),
    ])  # Статус транспортного средства
    driver = models.OneToOneField(Driver, on_delete=models.CASCADE, related_name='vehicle', null=True)  # Водитель
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE, related_name='vehicles', null=True, blank=True)  # Тип транспорта, теперь можно быть пустым

    def __str__(self):
        return f'{self.vehicle_number} - {self.vehicle_type.name if self.vehicle_type else "Unknown"}'

    def get_routes(self):
        Route = apps.get_model('map', 'Route')  
        return Route.objects.filter(vehicles=self)


