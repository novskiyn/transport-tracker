# Generated by Django 5.1.7 on 2025-03-15 23:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        ('driver', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='driver',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to='driver.driver', verbose_name='Водитель'),
        ),
    ]
