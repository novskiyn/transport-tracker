from django.db import models

class Route(models.Model):
    name = models.CharField(max_length=100)
    start_point = models.CharField(max_length=255)
    end_point = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Trip(models.Model):
    vehicle = models.ForeignKey('tracking.Vehicle', related_name='trips', on_delete=models.CASCADE)  # Ленивая загрузка
    route = models.ForeignKey(Route, related_name='trips', on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vehicle} по маршруту {self.route} с {self.departure_time} до {self.arrival_time}"
