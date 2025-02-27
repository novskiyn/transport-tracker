from rest_framework import serializers
from .models import Driver, Vehicle, DriverReview

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

class DriverReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverReview
        fields = '__all__'
