from django.shortcuts import redirect
from django.http import HttpResponseForbidden

def guest_required(view_func):
    """
    Декоратор для ограничения доступа для пользователей, которые уже аутентифицированы.
    Если пользователь аутентифицирован, перенаправляем его на домашнюю страницу в зависимости от роли.
    """
    def _wrapped_view(request, *args, **kwargs):
        # Если пользователь аутентифицирован
        if request.user.is_authenticated:
            # Перенаправляем на домашнюю страницу в зависимости от роли
            if request.user.role == 'driver':
                return redirect(f'/driver/home/{request.user.id}')
            elif request.user.role == 'client':
                return redirect(f'/client/home/{request.user.id}')
            elif request.user.role == 'admin':
                return redirect(f'/admin/home/{request.user.id}')
            else:
                return redirect('/')  # Default redirection
        return view_func(request, *args, **kwargs)

    return _wrapped_view
