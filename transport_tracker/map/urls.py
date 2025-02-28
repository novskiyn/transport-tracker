from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RouteViewSet, TripViewSet, index

router = DefaultRouter()
router.register(r'routes', RouteViewSet)
router.register(r'trips', TripViewSet)

urlpatterns = [
    path('api', include(router.urls)),
    path('', index, name='index')
]
