document.addEventListener("DOMContentLoaded", function () {
    let video = document.getElementById("bg-video");

    // Замедление видео
    video.playbackRate = 0.2; // Максимально плавное замедление

    // Плавный переход между циклами видео
    video.addEventListener("ended", function () {
        video.classList.add("fade-out");  // Затемнение перед повтором
        setTimeout(() => {
            video.currentTime = 0;
            video.play();
            video.classList.remove("fade-out");
        }, 500); // Ждем перед повтором, чтобы избежать резкого перехода
    });
});
