document.addEventListener("DOMContentLoaded", () => {
    console.log("Сайт загружен!");
    // Плавная прокрутка по якорям (если она нужна)
    const scrollLinks = document.querySelectorAll('a[href^="#"]');
    for (const link of scrollLinks) {
        link.addEventListener('click', function (event) {
            event.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            targetElement.scrollIntoView({ behavior: 'smooth' });
        });
    }
});
