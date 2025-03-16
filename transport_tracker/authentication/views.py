from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render

User = get_user_model()

# Регистрация нового пользователя
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Получаем модель пользователя из настроек
User = get_user_model()

@api_view(['POST'])
def register_user(request):
    # Получаем данные из запроса
    username = request.data.get('username')
    password = request.data.get('password')
    confirm_password = request.data.get('confirm_password')
    contact_number = request.data.get('contact_number')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    email = request.data.get('email')

    # Проверка обязательных полей
    if not username or not password or not contact_number or not first_name or not last_name or not email:
        return Response({"error": "Все поля обязательны: имя пользователя, пароль, контактный номер, имя, фамилия и email."}, status=status.HTTP_400_BAD_REQUEST)

    # Проверка совпадения паролей
    if password != confirm_password:
        return Response({"error": "Пароли не совпадают"}, status=status.HTTP_400_BAD_REQUEST)

    # Проверка на существование пользователя
    if User.objects.filter(username=username).exists():
        return Response({"error": "Пользователь с таким именем уже существует"}, status=status.HTTP_400_BAD_REQUEST)

    # Создание пользователя с дополнительными полями
    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        email=email,
        contact_number=contact_number
    )
    
    # Создание JWT токенов для пользователя
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    return Response({
        "message": "Пользователь успешно зарегистрирован",
        "access_token": access_token,
        "refresh_token": str(refresh)
    }, status=status.HTTP_201_CREATED)




# Вход пользователя с использованием JWT
@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"error": "Имя пользователя и пароль обязательны"}, status=status.HTTP_400_BAD_REQUEST)

    # Аутентификация пользователя
    user = authenticate(request, username=username, password=password)

    if not user:
        return Response({"error": "Неверное имя пользователя или пароль"}, status=status.HTTP_401_UNAUTHORIZED)

    # Создание JWT токенов
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    return Response({
        'message': 'Успешный вход',
        'access_token': access_token,
        'refresh_token': str(refresh),
    })


# Страница регистрации (для рендеринга шаблона)
def register_page(request):
    return render(request, 'auth/register_page.html')


# Страница входа (для рендеринга шаблона)
def login_page(request):
    return render(request, 'auth/login_page.html')