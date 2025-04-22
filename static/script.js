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


// Hide the loader when the page finishes loading
window.addEventListener("pageshow", () => {
    setTimeout(() => {
      document.getElementById("loader").classList.add("hidden");
    }, 300); // Small delay for smoother fade-out
});
  
// Show loader on link clicks
document.addEventListener("DOMContentLoaded", () => {
    const loader = document.getElementById("loader");
    document.querySelectorAll("a").forEach(link => {
        link.addEventListener("click", e => {
            const target = link.getAttribute("target");
            const href = link.getAttribute("href");
            if (target !== "_blank" && href && !href.startsWith("#") && !href.startsWith("javascript:")) {
                loader.classList.remove("hidden");
            }
        });
    });
});
  
