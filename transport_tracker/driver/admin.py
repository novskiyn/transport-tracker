from django.contrib import admin
from .models import Driver, DriverReview

# Админка для модели Driver
class DriverAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'contact_number', 'rating', 'review_count', 'avatar')  # Добавлен аватар
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('rating',)

    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'contact_number', 'email', 'rating', 'review_count', 'avatar')
        }),
    )

# Админка для модели DriverReview
class DriverReviewAdmin(admin.ModelAdmin):
    list_display = ('driver', 'get_user_name', 'rating', 'created_at')  # Используем get_user_name для отображения имени пользователя
    search_fields = ('driver__first_name', 'driver__last_name', 'user__username', 'rating')
    list_filter = ('rating',)

    def get_user_name(self, obj):
        return obj.user.username  # Получаем имя пользователя
    get_user_name.short_description = 'Пользователь'  # Указываем описание для столбца

# Регистрация моделей в админк
admin.site.register(Driver, DriverAdmin)
admin.site.register(DriverReview, DriverReviewAdmin)

