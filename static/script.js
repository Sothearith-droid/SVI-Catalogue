const loader = document.getElementById("loader");

const hideLoader = () => {
    if (loader) {
        loader.classList.add("hidden");
    }
};

// 1. Hide loader when the page fully loads
window.addEventListener("load", () => {
    setTimeout(hideLoader, 300);
});

// 2. Hide loader if page was loaded from back/forward cache
window.addEventListener("pageshow", (event) => {
    if (event.persisted || performance.getEntriesByType("navigation")[0]?.type === "back_forward") {
        hideLoader();
    }
});

// 3. Show loader on link clicks for page navigation
document.querySelectorAll("a").forEach(link => {
    link.addEventListener("click", e => {
        const href = link.getAttribute("href");
        const target = link.getAttribute("target");

        if (
            href &&
            !href.startsWith("#") &&
            !href.startsWith("javascript:") &&
            target !== "_blank"
        ) {
            loader.classList.remove("hidden");
        }
    });
});

// Category swiper
document.addEventListener("DOMContentLoaded", function () {
    const swiper = new swiper(".homeSwiper", {
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
    const swiper = new swiper('.productSwiper', {
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
