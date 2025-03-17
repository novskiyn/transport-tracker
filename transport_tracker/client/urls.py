from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, ClientReviewViewSet
from .views import home_page_client, about_page_client, contact_page_client, reviews_page_client, history_page_client, profile_page_client, map_page_client

router = DefaultRouter()

router.register(r'clients', ClientViewSet)
router.register(r'client-reviews', ClientReviewViewSet)

urlpatterns = [
    # API роуты
    path('api/', include(router.urls)),

    # Путь для страницы дома водителя с ID
    path('home/<int:user_id>/', home_page_client, name='home_page_client'),
    
    # Другие страницы водителя, все с параметром driver_id
    path('about/<int:user_id>/', about_page_client, name='about_page_client'),
    path('contact/<int:user_id>/', contact_page_client, name='contact_page_client'),
    path('reviews/<int:user_id>/', reviews_page_client, name='reviews_page_client'),
    path('history/<int:user_id>/', history_page_client, name='history_page_client'),
    path('profile/<int:user_id>/', profile_page_client, name='profile_page_client'),
    path('map/<int:user_id>/', map_page_client, name='map_page_client'),
]
