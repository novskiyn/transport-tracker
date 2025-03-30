from django import forms
from .models import Driver, DriverReview
from tracking.models import CompanyReview
from django.contrib.auth.models import User

# Форма для добавления или редактирования водителей
class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['first_name', 'last_name', 'contact_number']  # Изменил, чтобы использовать все необходимые поля

class DriverProfileForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['first_name', 'last_name', 'email', 'contact_number', 'avatar']  # Добавляем поле avatar

# Форма для обновления аватара водителя
class AvatarUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['avatar']

# Форма для обновления данных профиля пользователя (для водителя)
class ProfileUpdateForm(forms.ModelForm):
    contact_number = forms.CharField(max_length=20, required=False, label="Телефон")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

# Форма для добавления или редактирования отзыва для водителя
class DriverReviewForm(forms.ModelForm):
    # Поле рейтинга с выбором от 1 до 5
    rating = forms.ChoiceField(choices=[(i, str(i)) for i in range(1, 6)], widget=forms.RadioSelect)
    
    class Meta:
        model = DriverReview
        fields = ['driver', 'client', 'rating', 'comment']

class CompanyReviewForm(forms.ModelForm):
    class Meta:
        model = CompanyReview
        fields = ['rating', 'review_text']        

