from django.shortcuts import render
from tracking.models import VehicleType

def home_page(request):
    return render(request, 'user/home_page.html')

# Страница о компании (с информацией о транспортных средствах)
def about_page(request):
    transport_info = VehicleType.objects.all()
    return render(request, 'user/about_page.html', {'transport_info': transport_info})

# Страница контактов
def contact_page(request):
    return render(request, 'user/contact_page.html')

# Страница отзывов
def reviews_page(request):
    return render(request, 'user/reviews_page.html')
