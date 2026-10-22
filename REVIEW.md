# Tercera edición — lanzamiento del 25 de noviembre de 2026

Rama `redesign/tercera-edicion`, creada desde el estado publicado de `main`
(`8f76ee4`, PR #3). El usuario aprobó visualmente esta composición y autorizó su publicación en
producción después de confirmar la fecha, las pruebas y los controles del PR.

## Composición

- «De comprender a transformar» permanece exactamente igual: título, párrafos,
  frase destacada, ilustración, dos columnas, colores, tipografía y espaciado.
- El fundamento conserva únicamente la etiqueta y el título aprobado sobre
  elevar el nivel de conciencia. Mantiene el fondo salvia, queda centrado y usa
  un ancho máximo de 900 px. Padding vertical de 72 px en escritorio y 52 px en
  móvil; título de 36–42 px y 26–31 px respectivamente.
- Se retiraron los párrafos y la ilustración de madre e hija del fundamento,
  el bloque «Un entrenamiento diferente» y el bloque «¿Por qué un entrenamiento
  y no simplemente un curso?». No se trasladaron esos textos.
- Las tres tarjetas aparecen inmediatamente después del fundamento, con la
  pequeña etiqueta «LAS TRES ETAPAS DEL ENTRENAMIENTO». Se conservan exactamente
  sus textos, iconos, numeración, colores, medidas y distribución responsive.
- El hero y las vistas sociales dicen tercera edición. La portada muestra
  «3ª EDICIÓN · COMENZAMOS EL 25 DE NOVIEMBRE». `editionDate` y el atributo
  `datetime` del HTML indican `2026-11-25`; el FAQ confirma el día y el año.
  El script utiliza UTC y el HTML conserva un fallback sin JavaScript.

El resto de las secciones y recursos permanece intacto, incluidos modalidades,
WhatsApp y su mensaje, FAQ, Instagram, testimonios, Wistia, PayPal y `/bienvenida`.
La imagen retirada se conserva como archivo. No se agregan precios ni pagos
directos públicos. Solo se actualizó la referencia de inicio del FAQ para indicar la fecha
confirmada; las demás preguntas y respuestas se conservan.

## Desarrollo y verificación

HTML, CSS y JavaScript estáticos, sin framework ni compilación. Servir `Mi-web`:

```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory Mi-web
node --check Mi-web/config.js
node --check Mi-web/script.js
PYTHONDONTWRITEBYTECODE=1 python3 tools/check_landing.py --screenshots /tmp/recodifica-review
PYTHONDONTWRITEBYTECODE=1 python3 tools/check_welcome.py --screenshots /tmp/recodifica-review
git diff --check
```

Las dos suites pasaron: 11 escenarios de la landing y 9 de bienvenida. Incluyen
360, 390, 430, 768 y 1440 px, más 767 y 1024 px para la landing; contenido,
enlaces, número y mensaje de WhatsApp, ausencia de precios/checkout, hero,
VIP, FAQ, fotografías, ilustración, las cinco capturas y modales, zoom, teclado,
gesto táctil, movimiento reducido y funcionamiento sin JavaScript/observer.
Wistia se bloquea deliberadamente en la suite para validar su fallback; no se
validan reproducción real, entrega en WhatsApp ni transacciones. No se envían
mensajes ni pagos.

Una auditoría adicional contra `8f76ee4` confirmó HTML idéntico en las secciones
protegidas, incluyendo la primera sección posterior al video y las tres etapas.
En 360, 390, 768 y 1440 px comprobó estilos y geometría de esas secciones, y la
comparación de capturas de la objeción dio píxeles idénticos en los cuatro anchos.
Se verificaron alturas, color salvia, centrado y transición de 60–110 px hasta
las tarjetas, sin espacio añadido para compensar el contenido retirado.

Reducción de altura respecto de producción: 1.516 px en 360, 1.452 px en 390,
982 px en 768 y 851 px en 1440. Capturas y resultados de esta tarea en
`/workspace/recodifica-tercera-review/`, fuera del repositorio.

## Revisión en Vercel

El push de esta rama genera un deployment **Preview**. Consultar el deployment
del commit de la rama y abrir su URL. El Preview puede exigir una sesión de Vercel;
la pantalla de login no es una comprobación visual de la landing. No cambiar esa
protección. Tras completar las verificaciones y controles, fusionar el PR a `main` y
confirmar el deployment Production completado y el contenido de la URL oficial.
No cambiar la configuración de pagos ni promover manualmente otro deployment.

## Recursos optimizados

Las fotografías originales se conservan sin cambios. Ambas eran PNG aunque sus
nombres terminaban en `.jpg`. Las versiones WebP nuevas pesan 88.050 bytes (hero,
1122 × 1402) y 32.020 bytes (mentor, 720 × 900), frente a 3.853.351 bytes originales
en conjunto. El hero tiene prioridad de carga y el mentor carga diferida.

Las ilustraciones PNG originales se conservan intactas. Las versiones WebP
transparentes nuevas miden 680 × 453 y pesan 95.836 bytes (`reaccion-consciente`)
y 68.312 bytes (`nueva-percepcion`), frente a 3.584.602 bytes de los PNG. En la
tercera edición se muestra solo `reaccion-consciente`, con carga diferida y
proporción reservada. El segundo recurso se conserva en disco sin mostrarse
en el fundamento.

Montserrat se sirve localmente como WOFF2 variable latino (regular e itálica),
con `font-display: swap`. Fuente: `@fontsource-variable/montserrat@5.3.0`, obtenida
del registro npm. El archivo descargado se verificó con el SHA-512 publicado:

```text
sha512-7PaZoxaxrWLAyrhO46v65An9LhUhfkTExWLhfbywYZCnZEgg/W1rEHnlNmZKjNZ3nJTVYyicqxlJt10z/26yTA==
```

Licencia OFL incluida en `Mi-web/assets/fonts/LICENSE`. No se añadieron paquetes
al proyecto, píxeles, trackers ni un SDK de pago.
