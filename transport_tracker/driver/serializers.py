from rest_framework import serializers
from .models import Driver, DriverReview

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'

class DriverReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverReview
        fields = '__all__'
