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


document.addEventListener("DOMContentLoaded", () => {
    const loader = document.getElementById("loader");
  
    // Hide loader on full load
    window.addEventListener("load", () => {
      setTimeout(() => {
        loader.classList.add("hidden");
      }, 300);
    });
  
    // If page is restored from bfcache (back/forward cache), hide loader immediately
    window.addEventListener("pageshow", event => {
      if (event.persisted) {
        loader.classList.add("hidden");
      }
    });
  
    // Show loader on link click for normal navigation
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
   
  
