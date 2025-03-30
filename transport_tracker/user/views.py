from django.shortcuts import render
from tracking.models import VehicleType, CompanyReview
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home_page(request):
    return render(request, 'user/home_page.html')

# Страница о компании (с информацией о транспортных средствах)
def about_page(request):
    transport_info = VehicleType.objects.all()
    return render(request, 'user/about_page.html', {'transport_info': transport_info})

# Страница контактов
def contact_page(request):
    return render(request, 'user/contact_page.html')

def reviews_page(request):
    # Получаем все отзывы о компании
    company_reviews = CompanyReview.objects.all()

    # Пагинация
    paginator = Paginator(company_reviews, 5)  # Количество отзывов на странице
    page = request.GET.get('page')

    try:
        result_page = paginator.page(page)
    except PageNotAnInteger:
        result_page = paginator.page(1)
    except EmptyPage:
        result_page = paginator.page(paginator.num_pages)

    # Возвращаем рендер страницы с отзывами
    return render(request, 'user/reviews_page.html', {
        'reviews': result_page  # Передаем отзывы с пагинацией
    })

