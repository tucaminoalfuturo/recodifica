/* This page coordinates manual verification; it never infers payment or plan
 * from its URL. The HTML link remains usable if either script fails to load.
 */
(() => {
  "use strict";
  const link = document.getElementById("welcome-whatsapp");
  const number = window.RECODIFICA_CONFIG?.whatsapp?.number;
  if (!link || !/^\d{8,15}$/.test(number || "")) return;
  const message = [
    "Hola Seba, acabo de realizar mi compra del entrenamiento Recodificá tu Reactividad por PayPal",
    "Mi nombre es:",
    "El plan que elegí es: Básico / VIP",
    "Te comparto mi comprobante de pago para coordinar mi ingreso al entrenamiento",
    "¡Muchas gracias!",
  ].join("\n\n");
  link.href = `https://wa.me/${number}?text=${encodeURIComponent(message)}`;
})();
