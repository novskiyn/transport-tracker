from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render

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

    user.role = 'client'  # Если роль хранится в поле role
    user.save()
    
    # Создание JWT токенов для пользователя
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    return Response({
        "message": "Пользователь успешно зарегистрирован",
        "access_token": access_token,
        "refresh_token": str(refresh)
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Проверка наличия данных
    if not username or not password:
        return Response({"error": "Необходимо указать имя пользователя и пароль."}, status=status.HTTP_400_BAD_REQUEST)

    # Аутентификация пользователя
    user = authenticate(username=username, password=password)

    if user is None:
        return Response({"error": "Неверные учетные данные."}, status=status.HTTP_400_BAD_REQUEST)

    # Явно входим в систему
    login(request, user)

    # Генерация токенов для аутентифицированного пользователя
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    # Определение роли пользователя
    role = user.role  # Допустим, вы добавили поле role для пользователя

    # Перенаправление в зависимости от роли
    if role == 'driver':
        redirect_url = f'/driver/home/{user.id}'
    elif role == 'client':
        redirect_url = f'/client/home/{user.id}'
    elif role == 'admin':
        redirect_url = f'/admin/home/{user.id}'
    else:
        redirect_url = '/'  # Default redirection

    return Response({
        "message": "Вход успешен.",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "redirect_url": redirect_url  # Включаем информацию о перенаправлении
    })



# Страница регистрации (для рендеринга шаблона)
def register_page(request):
    return render(request, 'auth/register_page.html')


# Страница входа (для рендеринга шаблона)
def login_page(request):
    return render(request, 'auth/login_page.html')