from django.contrib import admin
from .models import Vehicle, Driver, DriverReview  # Импорт моделей

class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        'vehicle_number', 
        'current_location', 
        'status', 
        'driver', 
        'brand', 
        'year_of_manufacture', 
        'last_updated'
    )
    search_fields = ('vehicle_number', 'driver__first_name', 'driver__last_name', 'brand')
    list_filter = ('status',)

class DriverAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'contact_number', 'rating', 'review_count')
    search_fields = ('first_name', 'last_name')

class DriverReviewAdmin(admin.ModelAdmin):
    list_display = ('driver', 'user', 'rating', 'created_at')
    search_fields = ('driver__first_name', 'driver__last_name', 'user__username', 'rating')
    list_filter = ('rating',)

# Регистрация моделей
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(DriverReview, DriverReviewAdmin)
