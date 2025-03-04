from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RouteViewSet, TripViewSet, home_page, about_page, contact_page


router = DefaultRouter()
router.register(r'routes', RouteViewSet)
router.register(r'trips', TripViewSet)

urlpatterns = [
    path('api', include(router.urls)),
    path('', home_page, name='home_page'),
    path('about/', about_page, name='about_page'),
    path('contact/', contact_page, name='contact_page'),
]
