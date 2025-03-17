document.addEventListener('DOMContentLoaded', function() {
    const logoutButton = document.getElementById('logoutButton');
    
    // Обработчик события клика
    logoutButton.addEventListener('click', function(event) {
        event.preventDefault();  // Останавливаем переход по ссылке

        // Получаем URL logout из атрибута data-logout-url
        const logoutUrl = logoutButton.getAttribute('data-logout-url');

        // Показываем окно с подтверждением
        if (confirm("Вы уверены, что хотите выйти?")) {
            // Если пользователь подтвердил, отправляем пользователя на URL для выхода
            window.location.href = logoutUrl;
        }
    });
});
