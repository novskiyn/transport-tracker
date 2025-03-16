from django.urls import path
from .views import home_page, about_page, contact_page, reviews_page

urlpatterns = [
    path('home', home_page, name='home_page'),
    path('about/', about_page, name='about_page'),
    path('contact/', contact_page, name='contact_page'),
    path('reviews/', reviews_page, name='reviews_page'),
]