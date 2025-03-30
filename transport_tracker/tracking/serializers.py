from rest_framework import serializers
from .models import Vehicle, VehicleType, Trip, Route, CompanyReview

class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = '__all__'

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'

    def validate(self, data):
        driver = data['vehicle'].driver  # Получаем водителя
        if not driver.can_take_trip(data['departure_time'], data['arrival_time']):
            raise serializers.ValidationError("Водитель не может выполнить несколько маршрутов в одно и то же время.")
        return data          

class CompanyReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyReview
        fields = '__all__'    
