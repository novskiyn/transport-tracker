from django.db import models
from django.conf import settings
from django.db.models import Avg, Count
from django.core.exceptions import ValidationError

class Client(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=100, null=True, blank=True)
    rating = models.FloatField(default=0)
    review_count = models.PositiveIntegerField(default=0)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client_profile')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def update_rating(self):
        # Получаем все отзывы клиента
        reviews = self.client_reviews.all()
        if reviews.exists():
            # Используем агрегацию для подсчета среднего рейтинга и количества отзывов
            aggregate = reviews.aggregate(avg_rating=Avg('rating'), review_count=Count('id'))
            self.rating = aggregate['avg_rating']
            self.review_count = aggregate['review_count']
        else:
            self.rating = 0
            self.review_count = 0
        self.save()

class ClientReview(models.Model):
    client = models.ForeignKey(Client, related_name='client_reviews', on_delete=models.CASCADE)
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='client_reviewed_by', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Проверка, что только водитель может оставить отзыв для клиента
        if self.driver.role != 'driver':
            raise ValidationError("Только водители могут оставлять отзывы для клиентов.")
        super().save(*args, **kwargs)
        # После сохранения отзыва обновляем рейтинг клиента
        self.client.update_rating()

    def __str__(self):
        return f"Отзыв для {self.client} от {self.driver.username}: {self.rating} звезд"
