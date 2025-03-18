function updateAvatarPreview(event) {
    var file = event.target.files[0];
    if (file) {
        // Проверка типа файла
        if (!file.type.startsWith('image/')) {
            alert('Пожалуйста, выберите изображение');
            return;
        }

        var reader = new FileReader();
        reader.onload = function(e) {
            var avatarImage = document.getElementById('avatar-image');
            avatarImage.src = e.target.result;  // Обновляем изображение аватара

            // Скрыть кнопку сохранить, показать кнопку удалить
            document.getElementById('save-avatar-btn').classList.add('hidden');
            document.getElementById('delete-avatar-btn').classList.remove('hidden');
        };

        reader.onerror = function() {
            alert('Ошибка при загрузке изображения');
        };

        reader.readAsDataURL(file);  // Чтение изображения как DataURL
    }
}

// Логика для кнопки "Удалить аватар"
document.getElementById('delete-avatar-btn')?.addEventListener('click', function() {
    // После удаления аватара, скрыть кнопку удалить и показать кнопку сохранить
    document.getElementById('save-avatar-btn').classList.remove('hidden');
    document.getElementById('delete-avatar-btn').classList.add('hidden');
});

// Закрытие всех форм перед открытием нужной
function toggleForm(formClass) {
    // Закрытие всех форм с классами edit-profile-form и change-password-section
    document.querySelectorAll('.edit-profile-form, .change-password-section').forEach(f => {
        if (!f.classList.contains(formClass)) {
            f.classList.add('hidden');
        }
    });

    // Переключаем видимость выбранной формы с добавлением анимации
    var form = document.getElementById(formClass);
    form.classList.toggle('hidden');
}

// Авто-скрытие сообщений через 3 секунды с анимацией
setTimeout(function() {
    var messages = document.querySelectorAll('.message');
    messages.forEach(function(message) {
        message.style.transition = 'opacity 0.5s ease-out';  // Плавное исчезновение
        message.style.opacity = "0";
        setTimeout(() => {
            message.style.display = "none";  // Прячем сообщение после исчезновения
        }, 500);
    });
}, 3000);
