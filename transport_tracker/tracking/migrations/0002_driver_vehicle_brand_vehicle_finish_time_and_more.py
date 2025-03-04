# Generated by Django 5.1.6 on 2025-02-27 18:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('contact_number', models.CharField(max_length=15)),
                ('rating', models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='vehicle',
            name='brand',
            field=models.CharField(default='Unknown', max_length=50),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='finish_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='year_of_manufacture',
            field=models.PositiveIntegerField(default=2023),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='driver',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehicle', to='tracking.driver'),
        ),
    ]
