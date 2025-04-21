// Category swiper
document.addEventListener("DOMContentLoaded", function () {
const swiper = new Swiper(".homeSwiper", {
    loop: true,
    speed: 1000,
    autoplay: {
    delay: 3000,
    disableOnInteraction: false,
    },
    pagination: {
    el: ".swiper-pagination",
    clickable: true,
    },
    navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
    },
});
});


// Product swiper
document.addEventListener("DOMContentLoaded", function () {
    const swiper = new Swiper('.productSwiper', {
        loop: true,
        speed: 1000,
        slidesPerView: 1,
        spaceBetween: 10,
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
    });
});
