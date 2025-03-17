// Функция для отображения сообщения об ошибке
function showError(message) {
    const errorMessageElement = document.getElementById('error-message');
    errorMessageElement.innerText = message;
    errorMessageElement.style.display = 'block';
    document.getElementById('success-message').style.display = 'none';  // Скрыть сообщение об успехе
}

// Функция для отображения сообщения об успехе
function showSuccess(message) {
    const successMessageElement = document.getElementById('success-message');
    successMessageElement.innerText = message;
    successMessageElement.style.display = 'block';
    document.getElementById('error-message').style.display = 'none';  // Скрыть сообщение об ошибке
}

// Функция для получения CSRF токена из cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Обработчик отправки формы регистрации
document.getElementById('registerForm')?.addEventListener('submit', function (event) {
    event.preventDefault();

    const formData = new FormData(this);
    const data = {
        username: formData.get('username'),
        password: formData.get('password'),
        confirm_password: formData.get('confirm_password'),
        first_name: formData.get('first_name'),
        last_name: formData.get('last_name'),
        email: formData.get('email'),
        contact_number: formData.get('contact_number'),
    };

    // Проверка совпадения паролей
    if (data.password !== data.confirm_password) {
        showError('Пароли не совпадают!');
        return;
    }

    const csrfToken = getCookie('csrftoken');
    if (!csrfToken) {
        showError('Ошибка CSRF токена');
        return;
    }

    fetch('/auth/api/register/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,  // Получаем CSRF токен
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showError(data.error);
        } else {
            showSuccess(data.message);

            // Сохраняем токены в localStorage
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('refresh_token', data.refresh_token);
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        showError('Произошла ошибка при регистрации.');
    });
});

// Обработчик отправки формы входа
document.getElementById('loginForm')?.addEventListener('submit', function (event) {
    event.preventDefault();

    // Собираем данные из формы
    const formData = new FormData(this);
    const data = {
        username: formData.get('username'),
        password: formData.get('password'),
    };

    // Получаем CSRF токен
    const csrfToken = getCookie('csrftoken');
    if (!csrfToken) {
        showError('Ошибка CSRF токена');
        return;
    }

    // Отправка данных на сервер для аутентификации
    fetch('/auth/api/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,  // CSRF токен
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Ответ от сервера:', data);  // Добавьте этот лог для проверки ответа

        // Если ошибка, показываем сообщение
        if (data.error) {
            showError(data.error);
        } else {
            // В случае успеха
            showSuccess(data.message);

            // Сохраняем токены в localStorage
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('refresh_token', data.refresh_token);

            // Перенаправляем пользователя на нужную страницу
            window.location.href = data.redirect_url;
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        showError('Произошла ошибка при входе.');
    });
});
