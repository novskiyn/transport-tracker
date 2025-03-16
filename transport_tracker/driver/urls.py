from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DriverViewSet, DriverReviewViewSet
from .views import home_page_driver, about_page_driver, contact_page_driver, reviews_page_driver, history_page_driver, profile_page_driver, map_page_driver

router = DefaultRouter()

router.register(r'drivers', DriverViewSet)
router.register(r'driver-reviews', DriverReviewViewSet)

urlpatterns = [
    # API роуты
    path('api/', include(router.urls)),

    # Путь для страницы дома водителя с ID
    path('home/<int:user_id>/', home_page_driver, name='home_page_driver'),
    
    # Другие страницы водителя, все с параметром driver_id
    path('about/<int:user_id>/', about_page_driver, name='about_page_driver'),
    path('contact/<int:user_id>/', contact_page_driver, name='contact_page_driver'),
    path('reviews/<int:user_id>/', reviews_page_driver, name='reviews_page_driver'),
    path('history/<int:user_id>/', history_page_driver, name='history_page_driver'),
    path('profile/<int:user_id>/', profile_page_driver, name='profile_page_driver'),
    path('map/<int:user_id>/', map_page_driver, name='map_page_driver'),
]
