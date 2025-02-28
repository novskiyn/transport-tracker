from rest_framework import serializers
from .models import Route, Trip

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'

    def validate(self, data):
        # Проверка, что водителю не назначены другие поездки на этот промежуток времени
        driver = data['vehicle'].driver  # Получаем водителя
        if not driver.can_take_trip(data['departure_time'], data['arrival_time']):
            raise serializers.ValidationError("Водитель не может выполнить несколько маршрутов в одно и то же время.")
        return data    
