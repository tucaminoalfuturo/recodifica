/* Editable settings; no secrets. HTML has real fallbacks without JavaScript.
 * Update the matching HTML fallback if an integration or date changes.
 */
window.RECODIFICA_CONFIG = {
  editionDate: "2026-10-14",
  wistiaMediaId: "ruy9yzgati",
  paypal: {
    basic: "https://www.paypal.com/ncp/payment/J62F4J94WSUUS",
    vip: "https://www.paypal.com/ncp/payment/KCD2MNCN69K6C",
  },
  whatsapp: {
    number: "59897988262",
    message:
      "Hola, quiero consultar por otro medio de pago para Recodificá tu Reactividad",
  },
  // Supply the actual, anonymized originals in assets/testimonios/.
  // src stays null until the original file is available; never generate chat replicas.
  // Set publicationApproved only after consent for publishing is confirmed.
  testimonials: [
    {
      label: "Transformación profunda",
      src: null,
      publicationApproved: false,
      width: 833,
      height: 1449,
      alt: "Mensaje original: No tengo palabras para agradecer todo lo que viví en este entrenamiento.",
    },
    {
      label: "Reconexión personal",
      src: null,
      publicationApproved: false,
      width: 705,
      height: 459,
      alt: "Comentario original anónimo: Yo hice este entrenamiento y Woow, lo super recomiendo.",
    },
    {
      label: "Amor y compasión",
      src: null,
      publicationApproved: false,
      width: 825,
      height: 865,
      alt: "Mensaje original: Este entrenamiento te hace volver a mirarte con ojos de amor y compasión.",
    },
    {
      label: "Transformación familiar",
      src: null,
      publicationApproved: false,
      width: 800,
      height: 742,
      alt: "Mensaje original: De verdad que este entrenamiento lo recomiendo mucho.",
    },
    {
      label: "El impacto de escuchar al mentor",
      src: null,
      publicationApproved: false,
      width: 800,
      height: 390,
      alt: "Reacción original a un video: Llevo 30 minutos aproximadamente de video y cada palabra que dijiste hizo un movimiento en mí.",
    },
  ],
};
