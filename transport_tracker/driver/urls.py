from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DriverViewSet, DriverReviewViewSet

router = DefaultRouter()

router.register(r'drivers', DriverViewSet)
router.register(r'driver-reviews', DriverReviewViewSet)

urlpatterns = [
    # API роуты
    path('api/', include(router.urls)),
]
