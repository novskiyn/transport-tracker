from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RouteViewSet, TripViewSet

router = DefaultRouter()
router.register(r'routes', RouteViewSet)
router.register(r'trips', TripViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
