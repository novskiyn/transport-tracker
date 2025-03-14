from django.urls import path
from .views import register_user, login_user, register_page, login_page

urlpatterns = [
    path('register/', register_page, name='register_page'),
    path('login/', login_page, name='login_page'),
    path('api/register/', register_user, name='register_user'),
    path('api/login/', login_user, name='login_user'),
]
