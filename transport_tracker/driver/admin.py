from django.contrib import admin
from .models import Driver, DriverReview

class DriverAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'contact_number', 'rating', 'review_count')
    search_fields = ('first_name', 'last_name')
    list_filter = ('rating',)

class DriverReviewAdmin(admin.ModelAdmin):
    list_display = ('driver', 'user', 'rating', 'created_at')
    search_fields = ('driver__first_name', 'driver__last_name', 'user__username', 'rating')
    list_filter = ('rating',)

# Регистрация моделей в админк
admin.site.register(Driver, DriverAdmin)
admin.site.register(DriverReview, DriverReviewAdmin)

