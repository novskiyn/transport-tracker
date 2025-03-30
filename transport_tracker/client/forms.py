from django import forms
from .models import Client, ClientReview
from tracking.models import CompanyReview
from django.contrib.auth.models import User

# Форма для добавления или редактирования клиента
class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'email', 'contact_number']

class AvatarUpdateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['avatar']            

# Форма для добавления или редактирования отзывов для клиента
class ClientReviewForm(forms.ModelForm):
    # Поле рейтинга с выбором от 1 до 5
    rating = forms.ChoiceField(choices=[(i, str(i)) for i in range(1, 6)], widget=forms.RadioSelect)
    
    class Meta:
        model = ClientReview
        fields = ['client', 'driver', 'rating', 'comment']

class ProfileUpdateForm(forms.ModelForm):
    contact_number = forms.CharField(max_length=20, required=False, label="Телефон")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']        

class CompanyReviewForm(forms.ModelForm):
    class Meta:
        model = CompanyReview
        fields = ['rating', 'review_text']