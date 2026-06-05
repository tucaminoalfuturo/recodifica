/**
 * Recodifica tu Reactividad — Sebastián Baracco
 * script.js · v20260604
 * Vanilla JS puro · IIFE · sin módulos ES
 */
(function () {
  "use strict";

  /* ================================================================
     UTILIDAD: envuelve cada init en try/catch para que un error
     no rompa el resto del boot.
  ================================================================ */
  function safe(fn, name) {
    try {
      fn();
    } catch (e) {
      console.warn("[" + name + "]", e);
    }
  }


  /* ================================================================
     SCROLL REVEAL — IntersectionObserver
     Threshold muy bajo (0.04) + safety net a los 5s.
  ================================================================ */
  function initReveal() {
    var items = document.querySelectorAll(".reveal");
    if (!items.length) return;

    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) {
            e.target.classList.add("is-visible");
            io.unobserve(e.target);
          }
        });
      },
      {
        threshold: 0.04,
        rootMargin: "0px 0px -4% 0px",
      }
    );

    items.forEach(function (el) {
      io.observe(el);
    });

    /* Safety net: forzar visibilidad de cualquier elemento
       que siga oculto a los 5 segundos (scroll rápido, CPU lenta, etc.) */
    setTimeout(function () {
      document.querySelectorAll(".reveal:not(.is-visible)").forEach(function (el) {
        var rect = el.getBoundingClientRect();
        if (rect.top < window.innerHeight + 200) {
          el.classList.add("is-visible");
        }
      });
    }, 5000);
  }


  /* ================================================================
     HERO: zoom de entrada y observe de carga de imagen
  ================================================================ */
  function initHero() {
    var bg = document.querySelector(".hero-bg");
    if (!bg) return;

    /* Activa la imagen y el efecto de zoom una vez cargada */
    var heroImg = new Image();
    var bgStyle = bg.style.backgroundImage.replace(/url\(["']?|["']?\)/g, "");
    heroImg.onload = function () {
      bg.classList.add("loaded");
    };
    heroImg.src = bgStyle;

    /* Si no hay imagen (src vacío o rota), agregamos loaded igual */
    heroImg.onerror = function () {
      bg.classList.add("loaded");
    };
  }


  /* ================================================================
     SCROLL SUAVE para enlaces âncora (CTA → #oferta, etc.)
  ================================================================ */
  function initSmoothScroll() {
    document.addEventListener("click", function (e) {
      var a = e.target.closest('a[href^="#"]');
      if (!a) return;
      var id = a.getAttribute("href");
      if (!id || id === "#") return;
      var target = document.querySelector(id);
      if (!target) return;

      e.preventDefault();
      var navOffset = 0;   /* no hay nav fija en esta página */
      window.scrollTo({
        top: target.getBoundingClientRect().top + window.scrollY - navOffset,
        behavior: "smooth",
      });
    });
  }


  /* ================================================================
     ACORDEÓN — FAQ
  ================================================================ */
  function initAccordion() {
    var items = document.querySelectorAll(".accordion-item");
    if (!items.length) return;

    items.forEach(function (item) {
      var btn = item.querySelector(".accordion-btn");
      if (!btn) return;

      btn.addEventListener("click", function () {
        var isOpen = item.classList.contains("open");

        /* Cerrar todos los demás */
        items.forEach(function (other) {
          if (other !== item) {
            other.classList.remove("open");
            var otherBtn = other.querySelector(".accordion-btn");
            if (otherBtn) otherBtn.setAttribute("aria-expanded", "false");
          }
        });

        /* Toggle el actual */
        item.classList.toggle("open", !isOpen);
        btn.setAttribute("aria-expanded", String(!isOpen));
      });
    });
  }


  /* ================================================================
     MODALES PAYPAL
     openModal / closeModal son funciones globales (llamadas desde HTML).
     paypalRendered evita renderizar los botones dos veces.
  ================================================================ */
  var paypalRendered = { "modal-50": false, "modal-100": false };

  function openModal(id) {
    var overlay = document.getElementById(id);
    if (!overlay) return;

    overlay.removeAttribute("hidden");
    /* Doble requestAnimationFrame para que la transición CSS tenga tiempo */
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        overlay.classList.add("is-open");
      });
    });

    document.body.style.overflow = "hidden";

    /* Foco en el primer elemento interactivo del modal (accesibilidad) */
    var closeBtn = overlay.querySelector(".modal-close");
    if (closeBtn) setTimeout(function () { closeBtn.focus(); }, 50);

    /* Renderizar botones PayPal si el SDK está disponible */
    safe(function () { renderPayPalButtons(id); }, "renderPayPal:" + id);
  }

  function closeModal(id) {
    var overlay = document.getElementById(id);
    if (!overlay) return;

    overlay.classList.remove("is-open");

    /* Esperar a que termine la transición antes de ocultar */
    overlay.addEventListener(
      "transitionend",
      function handler() {
        overlay.setAttribute("hidden", "");
        overlay.removeEventListener("transitionend", handler);
        document.body.style.overflow = "";
      },
      { once: true }
    );
  }

  /* Cerrar modal al hacer clic en el overlay (fuera de la tarjeta) */
  function initModalClose() {
    document.querySelectorAll(".modal-overlay").forEach(function (overlay) {
      overlay.addEventListener("click", function (e) {
        if (e.target === overlay) {
          closeModal(overlay.id);
        }
      });
    });

    /* Cerrar con tecla Escape */
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") {
        document.querySelectorAll(".modal-overlay.is-open").forEach(function (o) {
          closeModal(o.id);
        });
      }
    });
  }

  /* Exponer al scope global para los botones onclick del HTML */
  window.openModal = openModal;
  window.closeModal = closeModal;


  /* ================================================================
     PAYPAL — renderiza botones dentro de cada modal

     CONFIGURACIÓN (completar con datos reales):
     1. Descomentá el script de PayPal en index.html
     2. Reemplazá YOUR_PAYPAL_CLIENT_ID con tu Client ID real
     3. Para recibir pagos reales usá el Live Client ID
     4. Para pruebas usá el Sandbox Client ID

     DOCS: https://developer.paypal.com/sdk/js/
  ================================================================ */
  function renderPayPalButtons(modalId) {
    /* Precio y contenedor según qué modal se abrió */
    var config = {
      "modal-50": {
        containerId: "paypal-buttons-50",
        amount: "50.00",
        description: "Recodifica tu Reactividad — Entrenamiento 30 días",
      },
      "modal-100": {
        containerId: "paypal-buttons-100",
        amount: "100.00",
        description: "Recodifica tu Reactividad — Entrenamiento VIP 30 días",
      },
    };

    var cfg = config[modalId];
    if (!cfg) return;

    /* No renderizar dos veces */
    if (paypalRendered[modalId]) return;

    var container = document.getElementById(cfg.containerId);
    if (!container) return;

    /* Si el SDK de PayPal no está cargado aún */
    if (!window.paypal) {
      container.innerHTML =
        '<p class="paypal-pending">' +
        "Para activar los pagos, configurá tu PayPal Client ID en el script de PayPal (ver comentarios en index.html).<br><br>" +
        '<a href="https://developer.paypal.com/dashboard/applications" target="_blank" rel="noopener">' +
        "Obtener mi Client ID →</a></p>";
      return;
    }

    /* Renderizar botones de PayPal */
    paypalRendered[modalId] = true;

    window.paypal
      .Buttons({
        style: {
          shape: "rect",
          color: "gold",
          layout: "vertical",
          label: "pay",
          height: 48,
        },

        /* Crear orden */
        createOrder: function (data, actions) {
          return actions.order.create({
            purchase_units: [
              {
                amount: {
                  value: cfg.amount,
                  currency_code: "USD",
                },
                description: cfg.description,
              },
            ],
          });
        },

        /* Pago aprobado */
        onApprove: function (data, actions) {
          return actions.order.capture().then(function (details) {
            closeModal(modalId);
            /* Mostrar mensaje de éxito */
            setTimeout(function () {
              showSuccessMessage(cfg.amount);
            }, 400);
          });
        },

        /* Error */
        onError: function (err) {
          console.error("PayPal error:", err);
          var errEl = document.createElement("p");
          errEl.className = "paypal-pending";
          errEl.textContent =
            "Hubo un problema al procesar el pago. Por favor intentá de nuevo o escribinos por WhatsApp.";
          container.appendChild(errEl);
        },

        /* Cancelación */
        onCancel: function () {
          /* El usuario cerró la ventana de PayPal — no hacer nada */
        },
      })
      .render("#" + cfg.containerId);
  }

  /* Mensaje de éxito después del pago */
  function showSuccessMessage(amount) {
    var overlay = document.createElement("div");
    overlay.style.cssText =
      "position:fixed;inset:0;z-index:1100;background:rgba(30,26,22,0.72);" +
      "display:flex;align-items:center;justify-content:center;padding:20px;";

    var card = document.createElement("div");
    card.style.cssText =
      "background:#fff;border-radius:16px;padding:48px 36px;max-width:420px;" +
      "width:100%;text-align:center;font-family:'Montserrat',sans-serif;";

    card.innerHTML =
      '<p style="font-size:2.5rem;margin-bottom:16px;">🎉</p>' +
      '<h3 style="font-size:1.3rem;font-weight:700;color:#2e2e2e;margin-bottom:12px;">¡Pago recibido!</h3>' +
      '<p style="font-size:0.9rem;color:#888;line-height:1.6;margin-bottom:28px;">' +
      "Gracias por tu inscripción. En breve recibirás un mensaje con todos los detalles del comienzo. " +
      "¡Bienvenida al entrenamiento!</p>" +
      '<button onclick="this.closest(\'[data-success]\').remove()" ' +
      'style="padding:14px 40px;background:#7d8767;color:#fff;border:none;border-radius:6px;' +
      'font-family:inherit;font-size:0.85rem;font-weight:700;letter-spacing:0.08em;cursor:pointer;">Cerrar</button>';

    overlay.dataset.success = "1";
    overlay.appendChild(card);
    document.body.appendChild(overlay);

    /* Cerrar al hacer clic en el overlay */
    overlay.addEventListener("click", function (e) {
      if (e.target === overlay) overlay.remove();
    });
  }


  /* ================================================================
     BOOT — arrancar todo cuando el DOM está listo
  ================================================================ */
  function boot() {
    safe(initReveal,      "initReveal");
    safe(initHero,        "initHero");
    safe(initSmoothScroll, "initSmoothScroll");
    safe(initAccordion,   "initAccordion");
    safe(initModalClose,  "initModalClose");
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }

})();
