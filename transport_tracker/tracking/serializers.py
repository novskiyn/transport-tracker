from rest_framework import serializers
from .models import Driver, Vehicle, DriverReview, VehicleType

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'

class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = '__all__'

class VehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = '__all__'

class DriverReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverReview
        fields = '__all__'
