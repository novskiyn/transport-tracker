from django.db import models
from django.contrib.auth.models import AbstractUser
from tracking.models import Driver
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    ROLE_CHOICES = [
        ('administrator', 'Администратор'),
        ('driver', 'Водитель'),
        ('client', 'Клиент'),
    ]
    
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='client')
    contact_number = models.CharField(max_length=15, blank=True, null=True)

    driver = models.OneToOneField(Driver, null=True, blank=True, on_delete=models.SET_NULL, related_name='user_profile', verbose_name="Водитель")  # Изменяем related_name

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


# Сигнал для автоматического создания водителя при сохранении пользователя
@receiver(post_save, sender=User)
def create_driver_for_user(sender, instance, created, **kwargs):
    if created and instance.role == 'driver' and not instance.driver:
        driver = Driver.objects.create(
            user=instance,
            first_name=instance.first_name,
            last_name=instance.last_name,
            email=instance.email,
            contact_number=instance.contact_number,
        )
        instance.driver = driver
        instance.save()


# Сигнал для обновления или удаления водителя, если роль пользователя изменяется
@receiver(post_save, sender=User)
def update_driver_for_user(sender, instance, **kwargs):
    if instance.role == 'driver' and not instance.driver:
        driver = Driver.objects.create(
            user=instance,
            first_name=instance.first_name,
            last_name=instance.last_name,
            email=instance.email,
            contact_number=instance.contact_number,
        )
        instance.driver = driver
        instance.save()

    elif instance.role != 'driver' and instance.driver:
        instance.driver.delete()
        instance.driver = None
        instance.save()
