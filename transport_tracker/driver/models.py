from django.db import models
from django.conf import settings
from django.db.models import Avg, Count
from django.core.exceptions import ValidationError
from django.db.models.signals import post_delete
from django.dispatch import receiver

class Driver(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=100, null=True, blank=True)  # Добавлено поле email
    rating = models.FloatField(default=0)
    review_count = models.PositiveIntegerField(default=0)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='driver_profile')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def update_rating(self):
        # Получаем средний рейтинг и количество отзывов для водителя
        reviews = self.reviews.all()
        if reviews.exists():
            # Используем агрегацию для подсчета суммы и количества отзывов
            aggregate = reviews.aggregate(avg_rating=Avg('rating'), review_count=Count('id'))
            self.rating = aggregate['avg_rating']
            self.review_count = aggregate['review_count']
        else:
            self.rating = 0
            self.review_count = 0
        self.save()

    def can_take_trip(self, departure_time, arrival_time):
        # Проверка на пересечение поездок водителя
        trips = Trip.objects.filter(vehicle__driver=self)
        for trip in trips:
            if (departure_time < trip.arrival_time and arrival_time > trip.departure_time):
                return False
        return True

class DriverReview(models.Model):
    driver = models.ForeignKey(Driver, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='driver_reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Проверяем, что отзыв может оставить только пользователь с ролью 'client'
        if self.user.role != 'client':
            raise ValidationError("Только клиенты могут оставлять отзывы.")
        super().save(*args, **kwargs)
        # После сохранения отзыва обновляем рейтинг водителя
        self.driver.update_rating()

    def __str__(self):
        return f"Отзыв о {self.driver} от {self.user.username}: {self.rating} звезд"


