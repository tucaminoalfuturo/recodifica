# Revisión de la segunda edición

Rama exclusiva: `redesign/segunda-edicion`. Refinamiento sobre los recursos
incorporados por el usuario en `779f72b`, para revisión mediante Vercel Preview.
Sin merge a `main` ni promoción a producción. Esta revisión también incorpora
los ajustes finales de contenido y una página de bienvenida para ambos planes.
La verificación de pagos continúa siendo personal, fuera del sitio.

## Desarrollo local

La landing sigue usando HTML, CSS y JavaScript sin framework, dependencias de
aplicación ni compilación. Servir la carpeta `Mi-web`, no la raíz del repositorio:

```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory Mi-web
```

La fecha de inicio y las integraciones se editan en `Mi-web/config.js`. Los enlaces
y la fecha tienen fallbacks reales en el HTML para navegadores sin JavaScript:
mantenerlos sincronizados al cambiar esos datos. La fecha de inicio se muestra
una sola vez; el FAQ remite a la portada.

## Integraciones y pendientes

- **Wistia:** ID oficial `ruy9yzgati`, SDK y módulo oficiales, carga al aproximarse
  al viewport, espacio reservado 16:9 y `auto-play="false"`. No se modifica la
  configuración de la barra de progreso. Se muestra un enlace alternativo si
  falla la carga. La política de red del entorno rechazó las consultas HTTPS a
  `fast.wistia.com`: reproducción, pausa y ajustes efectivos deben revisarse con
  acceso a Wistia antes de publicar. No se simuló reproducción en las pruebas.
- **PayPal:** los dos enlaces proporcionados están asociados a Básico y VIP, con
  apertura segura en otra pestaña. La política de red rechazó consultas HTTPS a
  `www.paypal.com`: verificar manualmente que el checkout muestre USD 50 para
  `J62F4J94WSUUS` y USD 100 para `KCD2MNCN69K6C`. No se iniciaron transacciones.
- **WhatsApp:** se conserva el número del código original, `59897988262`, con el
  mensaje solicitado. Se comprobó la URL y su codificación, sin enviar mensajes.
- **Testimonios:** cinco originales `.jpg` integrados, en el orden aprobado, con
  dimensiones reales y extractos intactos. Se verificó visualmente su correspondencia.
  El modal se probó con cada captura real: desplazamiento, zoom, teclado, Escape
  y retorno del foco. Los originales permanecen sin modificaciones. El área del
  autor de la segunda captura y las reacciones con iniciales de la tercera y
  cuarta se ocultan en la presentación. Ver `Mi-web/assets/testimonios/README.md`.

## Validación

El repositorio no contiene scripts de build, lint, typecheck ni una suite previa.
Se añadió una comprobación de navegador reproducible que usa Python Playwright
y Chromium disponibles en el entorno:

```sh
node --check Mi-web/config.js
node --check Mi-web/script.js
PYTHONDONTWRITEBYTECODE=1 python3 tools/check_landing.py --screenshots /tmp/recodifica-review
node --check Mi-web/bienvenida/script.js
PYTHONDONTWRITEBYTECODE=1 python3 tools/check_welcome.py --screenshots /tmp/recodifica-review
git diff --check
```

El script inicia y cierra su propio servidor temporal. Comprueba contenido y
precios, destinos de enlaces, formato 16:9, carga única del embed y su estado de
fallo, navegación al video, FAQ exclusivo, detalle VIP por teclado y carrusel
manual en 360, 390, 430, 768, 1440, 767 y 1024 px. En cada ancho prueba los cinco
modales reales, el zoom, el alcance del final del mensaje, las máscaras de
anonimización, carga y dimensiones de imágenes y ausencia de overflow. También
comprueba las entradas de animación una sola vez, movimiento reducido, la página
sin JavaScript, sin IntersectionObserver y un gesto táctil nativo en móvil.
Las solicitudes a Wistia se bloquean deliberadamente en esta suite para probar
el fallo de red; esto no valida reproducción real. No se navega al checkout ni
se realizan transacciones.

Resultado: los once escenarios de la suite pasaron. Además, se verificaron por
separado un fallo de carga del script y el cambio de preferencia a movimiento
reducido con la página abierta. En ambos casos el contenido permaneció accesible.
No se registraron excepciones de JavaScript. Capturas de los cinco anchos solicitados,
las secciones principales, modales y resultados en
`/workspace/recodifica-welcome-review/`, fuera del repositorio.

Antes de publicar: revisar el nuevo Preview en computadora y celular, comprobar
la reproducción real y confirmar los importes de los checkouts. El push se limita
a la rama de revisión; el estado del deployment se consulta en Vercel, en
Deployments, filtrando `redesign/segunda-edicion` y abriendo la última versión Preview.

## Refinamiento visual

Los cuatro bloques anteriores al método usan los nuevos textos aprobados. Se
conservan hero, mentor, las etapas, los cinco recursos, precios, FAQ, cierre y
configuración comercial. La primera ilustración se ubica debajo del título de
la objeción; la segunda acompaña el texto de conciencia. En escritorio miden
320 px de ancho y en móvil hasta 240 px. Ambas mantienen proporción y transparencia,
sin filtros, nuevos fondos, sombras ni resplandores añadidos.

Las entradas usan IntersectionObserver y Web Animations: opacidad, 14 px de
movimiento, 560 ms y 100 ms de separación entre tarjetas relacionadas. Se ejecutan
una sola vez. El estilo inicial del contenido siempre es visible; solo se anima
cuando entra en pantalla. El modo de movimiento reducido omite los efectos y
cancela los que estuvieran en ejecución. Hover discreto solo para dispositivos
con mouse: elevación de 2 px en tarjetas y respuesta en controles del carrusel.
No se añadieron bibliotecas.

Las capturas tienen vistas previas de 250 px en escritorio y 210 px en móvil,
sin deformación. La imagen completa se lee en el modal con scroll y zoom. Si el
script no carga, un `details` nativo permite leer cada testimonio completo.

## Recursos optimizados

Las fotografías originales se conservan sin cambios. Ambas eran PNG aunque sus
nombres terminaban en `.jpg`. Las versiones WebP nuevas pesan 88.050 bytes (hero,
1122 × 1402) y 32.020 bytes (mentor, 720 × 900), frente a 3.853.351 bytes originales
en conjunto. El hero tiene prioridad de carga y el mentor carga diferida.

Las ilustraciones PNG originales se conservan intactas. Las versiones WebP
transparentes nuevas miden 680 × 453 y pesan 95.836 bytes (`reaccion-consciente`)
y 68.312 bytes (`nueva-percepcion`), frente a 3.584.602 bytes de los PNG. Cargan
de forma diferida y se reserva su proporción.

Montserrat se sirve localmente como WOFF2 variable latino (regular e itálica),
con `font-display: swap`. Fuente: `@fontsource-variable/montserrat@5.3.0`, obtenida
del registro npm. El archivo descargado se verificó con el SHA-512 publicado:

```text
sha512-7PaZoxaxrWLAyrhO46v65An9LhUhfkTExWLhfbywYZCnZEgg/W1rEHnlNmZKjNZ3nJTVYyicqxlJt10z/26yTA==
```

Licencia OFL incluida en `Mi-web/assets/fonts/LICENSE`. No se añadieron paquetes
al proyecto, píxeles, trackers ni un SDK de pago.

## Ajustes finales y bienvenida

La introducción del video y su llamada centrada se actualizaron con los textos
solicitados. La llamada usa Montserrat semibold, 15–17 px y el oliva oscuro de
la marca para conservar contraste. La flecha permanece estática. Se eliminó
el texto sobre los 20 minutos, sin otro texto debajo del reproductor. Los
párrafos editoriales ya no terminan con punto; las oraciones internas conservan
su puntuación. Los extractos y originales de testimonios y su contexto siguen
intactos. Se eliminaron las promesas de audios diarios, se corrigió el nombre
visible y accesible a Sebastián Baracco y se actualizó Instagram a
`https://www.instagram.com/sebasbaracco`. Precios, PayPal y Wistia se conservan.

La nueva página está en `Mi-web/bienvenida/index.html`, acompañada por sus
propios `styles.css` y `script.js`. Reutiliza `/styles.css`, las variables de la
marca, el logotipo, el botón y Montserrat local. No carga el script de la landing
ni el reproductor. Vercel sirve `/bienvenida` mediante una reescritura a
`/bienvenida/index.html` en el archivo existente `Mi-web/vercel.json`; no se
creó otro proyecto. El servidor local sirve el mismo directorio estático con
una redirección normal de `/bienvenida` a `/bienvenida/`, sin errores 404.
Los recursos usan rutas desde la raíz para funcionar en ambos casos.

Es una sola página para Básico y VIP. El botón usa el número de
`RECODIFICA_CONFIG.whatsapp.number`, actualmente `59897988262`, con el nuevo
mensaje completo y sus saltos de línea. El nombre queda vacío y el campo de
plan ofrece Básico / VIP para que la participante lo edite en WhatsApp y
adjunte su comprobante manualmente. El HTML contiene un enlace equivalente
para fallos o ausencia de JavaScript. No se envían mensajes automáticamente.
La apertura de la página y los parámetros de URL nunca confirman un pago ni
asignan acceso a Telegram. El tercer paso comunica la verificación personal.

`tools/check_welcome.py` comprueba la ruta directa, los recursos locales, carga
real de Montserrat, contenido, tamaños del título, controles y ausencia de
scroll horizontal en los cinco anchos. Prueba foco visible, Enter y apertura
del destino de WhatsApp mediante navegación interceptada, con el mensaje y
número correctos. También verifica el enlace sin JavaScript, con fallos de
ambos scripts y con movimiento reducido, usando parámetros de URL ficticios
para asegurar que no infieren datos. Los nueve escenarios pasaron. No valida
la entrega de mensajes en la aplicación externa ni un deployment real.

Para revisar: abrir el último **Preview** de `redesign/segunda-edicion` en
Vercel → Deployments → Ready → Visit, y agregar `/bienvenida` a su dominio.
La raíz del mismo Preview muestra la landing. La URL definitiva de producción
no es la vista previa de esta tarea. Antes de publicar, revisar ambas páginas
en ese Preview. El retorno de PayPal se configurará posteriormente, cuando la
ruta se publique y se confirme que funciona en producción; no se cambió ahora.
