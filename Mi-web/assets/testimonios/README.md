# Capturas originales pendientes

Las cinco capturas se proporcionaron visualmente en el chat, pero sus archivos
originales no están accesibles en el entorno. No se recrearon imágenes ni mensajes.
Los extractos exactos sí están en el carrusel, en el orden aprobado.

Al disponer de los originales, guardarlos aquí con nombres claros:

1. `transformacion-profunda` — «No tengo palabras para agradecer…».
2. `reconexion-personal` — «Yo hice este entrenamiento y Woow…».
3. `amor-y-compasion` — «Este entrenamiento te hace volver a mirarte…».
4. `transformacion-familiar` — «De verdad que este entrenamiento…».
5. `impacto-del-video` — «Llevo 30 minutos aproximadamente de video…».

Usar únicamente originales con permiso para publicación y sin datos personales
identificables. Mantener íntegro el mensaje; ocultar nombres, usuarios, fotos,
teléfonos o iniciales identificativas sin recrear el chat.

En `Mi-web/config.js`, completar `testimonials[i].src` con una ruta relativa a
`Mi-web` (por ejemplo `assets/testimonios/transformacion-profunda.png`), registrar
las dimensiones reales y marcar `publicationApproved: true` cuando corresponda.
Esto añade automáticamente la miniatura y el botón para ampliarla en el modal.
El quinto mensaje se identifica como reacción a un video, no como finalización
del entrenamiento. No añadir la captura del programa de 90 días.
