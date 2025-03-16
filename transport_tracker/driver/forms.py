from django import forms
from .models import Driver, DriverReview

# Форма для добавления или редактирования водителей
class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['first_name', 'last_name', 'contact_number']  # Изменил, чтобы использовать все необходимые поля

# Форма для добавления или редактирования отзывов водителей
class DriverReviewForm(forms.ModelForm):
    # Список выбора рейтинга от 1 до 5
    rating = forms.ChoiceField(choices=[(i, str(i)) for i in range(1, 6)], widget=forms.RadioSelect)
    
    class Meta:
        model = DriverReview
        fields = ['driver', 'user', 'rating', 'comment']  # Включает поля для водителя, пользователя, рейтинга и комментария   
