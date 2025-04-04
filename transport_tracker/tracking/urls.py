from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehicleViewSet, VehicleTypeViewSet, RouteViewSet, TripViewSet, CompanyReviewViewSet

router = DefaultRouter()

# Регистрируем все viewsets
router.register(r'vehicles', VehicleViewSet)
router.register(r'vehicles-type', VehicleTypeViewSet)
router.register(r'routes', RouteViewSet)
router.register(r'trips', TripViewSet)
router.register(r'company-review', CompanyReviewViewSet)


urlpatterns = [
    # API роуты
    path('api/', include(router.urls)),
]
