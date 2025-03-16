from django.db import models
from django.contrib.auth.models import AbstractUser
from tracking.models import Driver
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken

class User(AbstractUser):
    ROLE_CHOICES = [
        ('administrator', 'Администратор'),
        ('driver', 'Водитель'),
        ('client', 'Клиент'),
    ]
    
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='client')
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    driver = models.OneToOneField(Driver, null=True, blank=True, on_delete=models.SET_NULL, related_name='user_profile', verbose_name="Водитель")
    access_token = models.CharField(max_length=255, blank=True, null=True)
    refresh_token = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    # Генерация токенов
    def generate_tokens(self):
        refresh = RefreshToken.for_user(self)
        self.access_token = str(refresh.access_token)
        self.refresh_token = str(refresh)
        self.save()

# Сигнал для автоматического создания или обновления водителя при изменении роли пользователя
@receiver(post_save, sender=User)
def handle_driver_for_user(sender, instance, created, **kwargs):
    if created:
        # Генерация токенов при создании пользователя
        instance.generate_tokens()

    if instance.role == 'driver':
        if created or not instance.driver:
            driver = Driver.objects.create(
                user=instance,
                first_name=instance.first_name,
                last_name=instance.last_name,
                email=instance.email,
                contact_number=instance.contact_number,
            )
            instance.driver = driver
            instance.save()
    else:
        if instance.driver:
            instance.driver.delete()
            instance.driver = None
            instance.save()
