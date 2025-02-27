from django.db import models
from django.apps import apps  
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


class Vehicle(models.Model):
    vehicle_number = models.CharField(max_length=50)
    current_location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('on_route', 'On Route'),
    ])
    last_updated = models.DateTimeField(auto_now=True)
    driver = models.OneToOneField(Driver, on_delete=models.CASCADE, related_name='vehicle', null=True)
    brand = models.CharField(max_length=50, default='Unknown')
    year_of_manufacture = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.vehicle_number

    def get_routes(self):
        Route = apps.get_model('map', 'Route')  
        return Route.objects.filter(vehicles=self)

