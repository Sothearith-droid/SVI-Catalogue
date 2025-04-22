document.addEventListener("DOMContentLoaded", () => {
    const loader = document.getElementById("loader");
    console.log("DOM loaded");

    const hideLoader = () => {
        if (loader) {
            console.log("Hiding loader");
            loader.classList.add("hidden");
        }
    };

    window.addEventListener("load", () => {
        console.log("Page fully loaded");
        setTimeout(hideLoader, 300);
    });

    window.addEventListener("pageshow", (event) => {
        console.log("Page show", event.persisted);
        if (event.persisted || performance.getEntriesByType("navigation")[0]?.type === "back_forward") {
            hideLoader();
        }
    });

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
                console.log("Navigating, showing loader for link:", href);
                loader.classList.remove("hidden");
            }
        });
    });

    // Category swiper
    new Swiper(".homeSwiper", {
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

    // Product swiper
    new Swiper('.productSwiper', {
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
