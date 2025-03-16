from django.contrib import admin
from .models import User

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'is_active', 'driver', 'contact_number', 'email', 'first_name', 'last_name')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'contact_number')}),  # Добавляем contact_number
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'contact_number')  # Добавляем поле в поиск
    ordering = ('username',)

admin.site.register(User, CustomUserAdmin)
