from django import forms
from .models import Vehicle, VehicleType, Route, Trip, CompanyReview

# Форма для добавления или редактирования транспортных средств
class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_number', 'current_location', 'status', 'driver', 'vehicle_type']  # Добавил vehicle_type

# Форма для добавления или редактирования типов транспорта
class VehicleTypeForm(forms.ModelForm):
    class Meta:
        model = VehicleType
        fields = ['name', 'brand', 'max_capacity', 'year_of_manufacture', 'description']  # Добавил все нужные поля для типа транспорта

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['name', 'start_point', 'end_point']

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['vehicle', 'route', 'departure_time', 'arrival_time']        

class CompanyReviewForm(forms.ModelForm):
    class Meta:
        model = CompanyReview
        fields = ['rating', 'review_text']    
