from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User  # Используйте вашу модель, если она отличается

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'role', 'is_active', 'driver', 'contact_number', 'email', 'first_name', 'last_name', 'access_token', 'refresh_token')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'contact_number')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'contact_number')
    ordering = ('username',)

    def save_model(self, request, obj, form, change):
        # Сохраняем пользователя
        super().save_model(request, obj, form, change)
        
        # Если это новый пользователь, создаем токены
        if not change:
            refresh = RefreshToken.for_user(obj)
            obj.access_token = str(refresh.access_token)
            obj.refresh_token = str(refresh)
            obj.save()

admin.site.register(User, CustomUserAdmin)
