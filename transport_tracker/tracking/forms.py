from django import forms
from .models import Vehicle, Driver, DriverReview, VehicleType, Route, Trip

# Форма для добавления или редактирования транспортных средств
class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_number', 'current_location', 'status', 'driver', 'vehicle_type']  # Добавил vehicle_type

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
