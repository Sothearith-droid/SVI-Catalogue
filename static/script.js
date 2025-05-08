document.addEventListener("DOMContentLoaded", () => {
    const loader = document.getElementById("loader");
    let loaderTimeout;

    const hideLoader = () => {
        if (loader) {
            loader.classList.remove("active");
            setTimeout(() => {
                loader.classList.add("hidden");
            }, 400);
        }
    };

    window.addEventListener("load", () => {
        setTimeout(hideLoader, 300);
    });

    window.addEventListener("pageshow", (event) => {
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
                target !== "_blank" &&
                !link.hasAttribute("data-fancybox")
            ) {
                clearTimeout(loaderTimeout);
                loaderTimeout = setTimeout(() => {
                    loader.classList.remove("hidden");
                    loader.classList.add("active");
                }, 300);
            }
        });
    });

    // Flickity carousel setup
//     const isMobile = window.innerWidth < 768;
//     const carousel = document.querySelector('.carousel');

//     if (carousel) {
//         new Flickity(carousel, {
//             wrapAround: true,
//             autoPlay: 3000,
//             prevNextButtons: false,
//             pageDots: true,
//             imagesLoaded: true,
//             draggable: isMobile
//         });
//     }
});
