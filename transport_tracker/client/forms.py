from django import forms
from .models import Client, ClientReview

# Форма для добавления или редактирования клиента
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'contact_number']

# Форма для добавления или редактирования отзывов для клиента
class ClientReviewForm(forms.ModelForm):
    # Поле рейтинга с выбором от 1 до 5
    rating = forms.ChoiceField(choices=[(i, str(i)) for i in range(1, 6)], widget=forms.RadioSelect)
    
    class Meta:
        model = ClientReview
        fields = ['client', 'driver', 'rating', 'comment']
