from django.contrib import admin
from .models import Client, ClientReview

class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'contact_number', 'email', 'rating', 'review_count')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('rating',)

class ClientReviewAdmin(admin.ModelAdmin):
    list_display = ('client', 'driver', 'rating', 'created_at')
    search_fields = ('client__first_name', 'client__last_name', 'driver__first_name', 'driver__last_name', 'rating')
    list_filter = ('rating',)

# Регистрация моделей в админке
admin.site.register(Client, ClientAdmin)
admin.site.register(ClientReview, ClientReviewAdmin)
