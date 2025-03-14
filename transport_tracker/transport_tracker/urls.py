
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from user.views import home_page, about_page, contact_page, reviews_page
from authentication.views import register_page, login_page
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('admin/', admin.site.urls),

    path('auth/', include('authentication.urls')),

    path('tracking/', include('tracking.urls')),

    path('user', include('user.urls')),

    path('', home_page, name='home_page'),
    path('about/', about_page, name='about_page'),
    path('contact/', contact_page, name='contact_page'),
    path('reviews/', reviews_page, name='reviews_page'),

    path('register/', register_page, name='register_page'),
    path('login/', login_page, name='login_page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
