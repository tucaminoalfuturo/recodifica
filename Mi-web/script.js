/* Vanilla JS; the content remains readable without JavaScript. */
(function () {
  "use strict";
  var config = window.RECODIFICA_CONFIG;
  var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  function initLinks() {
    if (!config) return;
    var date = document.getElementById("edition-date");
    var edition = new Date(config.editionDate + "T12:00:00Z");
    if (!Number.isNaN(edition.getTime())) {
      date.dateTime = config.editionDate;
      date.textContent = new Intl.DateTimeFormat("es-UY", {
        day: "numeric",
        month: "long",
        timeZone: "UTC",
      })
        .format(edition)
        .toUpperCase();
    }
    document.getElementById("paypal-basic").href = config.paypal.basic;
    document.getElementById("paypal-vip").href = config.paypal.vip;
    document.querySelectorAll("[data-whatsapp]").forEach(function (link) {
      link.href =
        "https://wa.me/" +
        config.whatsapp.number +
        "?text=" +
        encodeURIComponent(config.whatsapp.message);
    });
  }

  function initVideo() {
    var player = document.querySelector("wistia-player");
    var mediaId = config
      ? config.wistiaMediaId
      : player.getAttribute("media-id");
    player.setAttribute("media-id", mediaId);
    player.style.backgroundImage =
      "url('https://fast.wistia.com/embed/medias/" + mediaId + "/swatch')";
    customElements.whenDefined("wistia-player").then(function () {
      player.style.backgroundImage = "";
    });
    var loaded = false;
    function load() {
      if (loaded) return;
      loaded = true;
      [
        "https://fast.wistia.com/player.js",
        "https://fast.wistia.com/embed/" + mediaId + ".js",
      ].forEach(function (url, index) {
        var script = document.createElement("script");
        script.src = url;
        script.async = true;
        if (index === 1) script.type = "module";
        script.onerror = function () {
          document.getElementById("video-error").hidden = false;
        };
        document.head.appendChild(script);
      });
    }
    if ("IntersectionObserver" in window) {
      var observer = new IntersectionObserver(
        function (entries) {
          if (
            entries.some(function (entry) {
              return entry.isIntersecting;
            })
          ) {
            load();
            observer.disconnect();
          }
        },
        { rootMargin: "300px" },
      );
      observer.observe(player);
    } else load();
    document.getElementById("hero-cta").addEventListener("click", load);
  }

  function initTestimonials() {
    var track = document.getElementById("testimonials-track");
    var cards = Array.from(track.children);
    var previous = document.getElementById("testimonials-prev");
    var next = document.getElementById("testimonials-next");
    var position = document.getElementById("testimonials-position");
    var dialog = document.getElementById("testimonial-dialog");
    var fullImage = document.getElementById("testimonial-full-image");
    var returnFocus;
    document.querySelector(".carousel-controls").hidden = false;
    position.hidden = false;

    function activeIndex() {
      var start = track.getBoundingClientRect().left + 3;
      return cards.reduce(function (closest, card, index) {
        return Math.abs(card.getBoundingClientRect().left - start) <
          Math.abs(cards[closest].getBoundingClientRect().left - start)
          ? index
          : closest;
      }, 0);
    }
    function update() {
      var index = activeIndex();
      previous.disabled = track.scrollLeft < 5;
      next.disabled =
        track.scrollLeft + track.clientWidth >= track.scrollWidth - 5;
      position.textContent = index + 1 + " de " + cards.length;
    }
    function move(direction) {
      var index = Math.max(
        0,
        Math.min(cards.length - 1, activeIndex() + direction),
      );
      track.scrollTo({
        left: cards[index].offsetLeft - cards[0].offsetLeft,
        behavior: reducedMotion.matches ? "instant" : "smooth",
      });
    }
    previous.addEventListener("click", function () {
      move(-1);
    });
    next.addEventListener("click", function () {
      move(1);
    });
    track.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    track.addEventListener("keydown", function (event) {
      if (event.target !== track) return;
      if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
        event.preventDefault();
        move(event.key === "ArrowRight" ? 1 : -1);
      }
    });

    // Only attach supplied, anonymized original screenshots approved for publication.
    if (config)
      config.testimonials.forEach(function (item, index) {
        if (!item.src || !item.publicationApproved || !cards[index]) return;
        var button = document.createElement("button");
        button.className = "capture-button";
        button.type = "button";
        button.setAttribute("aria-haspopup", "dialog");
        button.setAttribute(
          "aria-label",
          "Ampliar captura original: " + item.label,
        );
        var image = document.createElement("img");
        image.src = item.src;
        image.alt = item.alt;
        image.width = item.width;
        image.height = item.height;
        image.loading = "lazy";
        image.decoding = "async";
        var caption = document.createElement("span");
        caption.textContent = "Ver captura completa";
        button.append(image, caption);
        button.addEventListener("click", function () {
          returnFocus = button;
          fullImage.src = item.src;
          fullImage.alt = item.alt;
          fullImage.width = item.width;
          fullImage.height = item.height;
          document.getElementById("testimonial-dialog-title").textContent =
            item.label;
          dialog.showModal();
          document.body.classList.add("modal-open");
          document.getElementById("testimonial-close").focus();
          document.querySelector(".dialog-image-scroll").scrollTop = 0;
        });
        cards[index].appendChild(button);
      });
    document
      .getElementById("testimonial-close")
      .addEventListener("click", function () {
        dialog.close();
      });
    dialog.addEventListener("click", function (event) {
      var rect = dialog.getBoundingClientRect();
      if (
        event.target === dialog &&
        (event.clientX < rect.left ||
          event.clientX > rect.right ||
          event.clientY < rect.top ||
          event.clientY > rect.bottom)
      )
        dialog.close();
    });
    dialog.addEventListener("close", function () {
      document.body.classList.remove("modal-open");
      if (returnFocus) returnFocus.focus();
    });
    dialog.addEventListener("keydown", function (event) {
      if (event.key !== "Tab") return;
      var controls = dialog.querySelectorAll('button, [tabindex="0"]');
      var first = controls[0];
      var last = controls[controls.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    });
    update();
  }

  // Native details supplies keyboard interaction and state without custom ARIA.
  // Keep one FAQ open at a time, including browsers without details[name].
  document.querySelectorAll(".accordion details").forEach(function (item) {
    item.addEventListener("toggle", function () {
      if (item.open)
        document
          .querySelectorAll(".accordion details")
          .forEach(function (other) {
            if (other !== item) other.open = false;
          });
    });
  });

  initLinks();
  initVideo();
  initTestimonials();
})();
