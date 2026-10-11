/* Editable settings; no secrets. Keep matching HTML fallbacks synchronized.
 * Testimonial width/height are the actual originals. displayHeight excludes only
 * identifying reaction badges; redactions conceal the author area, never messages.
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
      "Hola Seba, sentí que este entrenamiento resonó conmigo y quiero más información",
  },
  testimonials: [
    {
      label: "Transformación profunda",
      src: "assets/testimonios/testimonio-1.jpg",
      publicationApproved: true,
      width: 833,
      height: 1449,
      alt: "Mensaje original: No tengo palabras para agradecer todo lo que viví en este entrenamiento.",
    },
    {
      label: "Reconexión personal",
      src: "assets/testimonios/testimonio-2.jpg",
      publicationApproved: true,
      width: 705,
      height: 459,
      alt: "Comentario original anónimo: Yo hice este entrenamiento y Woow, lo super recomiendo.",
      redactions: [
        {
          x: 8,
          y: 28,
          width: 226,
          height: 39,
        },
      ],
    },
    {
      label: "Amor y compasión",
      src: "assets/testimonios/testimonio-3.jpg",
      publicationApproved: true,
      width: 825,
      height: 865,
      alt: "Mensaje original: Este entrenamiento te hace volver a mirarte con ojos de amor y compasión.",
      displayHeight: 745,
    },
    {
      label: "Transformación familiar",
      src: "assets/testimonios/testimonio-4.jpg",
      publicationApproved: true,
      width: 800,
      height: 742,
      alt: "Mensaje original: De verdad que este entrenamiento lo recomiendo mucho.",
      displayHeight: 650,
    },
    {
      label: "El impacto de escuchar al mentor",
      src: "assets/testimonios/testimonio-5.jpg",
      publicationApproved: true,
      width: 800,
      height: 390,
      alt: "Reacción original a un video: Llevo 30 minutos aproximadamente de video y cada palabra que dijiste hizo un movimiento en mí.",
    },
  ],
};
