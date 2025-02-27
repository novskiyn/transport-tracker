from django import forms
from .models import Route, Trip

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['name', 'start_point', 'end_point']

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['vehicle', 'route', 'departure_time', 'arrival_time']
