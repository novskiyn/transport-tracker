from django import forms
from .models import Vehicle, Driver, DriverReview

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_number', 'current_location', 'status', 'driver', 'brand', 'year_of_manufacture']

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['first_name', 'last_name', 'contact_number']

class DriverReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=[(i, str(i)) for i in range(1, 6)], widget=forms.RadioSelect)

    class Meta:
        model = DriverReview
        fields = ['driver', 'user', 'rating', 'comment']
