from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehicleViewSet, DriverViewSet, DriverReviewViewSet, VehicleTypeViewSet

router = DefaultRouter()
router.register(r'vehicles', VehicleViewSet)
router.register(r'vehicles-type', VehicleTypeViewSet)
router.register(r'drivers', DriverViewSet)
router.register(r'driver-reviews', DriverReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
