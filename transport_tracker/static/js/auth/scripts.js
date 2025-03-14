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
    };

    // Проверка совпадения паролей
    if (data.password !== data.confirm_password) {
        document.getElementById('error-message').innerText = 'Пароли не совпадают!';
        document.getElementById('error-message').style.display = 'block';
        return;
    }

    fetch('/auth/api/register/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),  // Получаем CSRF токен
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('error-message').innerText = data.error;
            document.getElementById('error-message').style.display = 'block';
            document.getElementById('success-message').style.display = 'none';
        } else {
            document.getElementById('success-message').innerText = data.message;
            document.getElementById('success-message').style.display = 'block';
            document.getElementById('error-message').style.display = 'none';

            // Сохраняем токены в localStorage
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('refresh_token', data.refresh_token);
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        document.getElementById('error-message').innerText = 'Произошла ошибка при регистрации.';
        document.getElementById('error-message').style.display = 'block';
    });
});

// Обработчик отправки формы входа
document.getElementById('loginForm')?.addEventListener('submit', function (event) {
    event.preventDefault();

    const formData = new FormData(this);
    const data = {
        username: formData.get('username'),
        password: formData.get('password'),
    };

    fetch('/auth/api/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),  // Получаем CSRF токен
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('error-message').innerText = data.error;
            document.getElementById('error-message').style.display = 'block';
            document.getElementById('success-message').style.display = 'none';
        } else {
            document.getElementById('success-message').innerText = data.message;
            document.getElementById('success-message').style.display = 'block';
            document.getElementById('error-message').style.display = 'none';

            // Сохраняем токены в localStorage
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('refresh_token', data.refresh_token);
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        document.getElementById('error-message').innerText = 'Произошла ошибка при входе.';
        document.getElementById('error-message').style.display = 'block';
    });
});

