from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render

# Регистрация нового пользователя
@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    confirm_password = request.data.get('confirm_password')

    if not username or not password:
        return Response({"error": "Имя пользователя и пароль обязательны"}, status=status.HTTP_400_BAD_REQUEST)

    if password != confirm_password:
        return Response({"error": "Пароли не совпадают"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Пользователь с таким именем уже существует"}, status=status.HTTP_400_BAD_REQUEST)

    # Создание пользователя
    user = User.objects.create_user(username=username, password=password)
    
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
    return render(request, 'user/register_page.html')


# Страница входа (для рендеринга шаблона)
def login_page(request):
    return render(request, 'user/login_page.html')
