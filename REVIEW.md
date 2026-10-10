# Revisión de la segunda edición

Rama: `redesign/segunda-edicion`. Cambios locales para revisión, sin push, merge ni
despliegue. La página de bienvenida y la confirmación de pagos quedan fuera de alcance.

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
- **Testimonios:** cinco extractos exactos y carrusel manual completos; archivos
  originales pendientes. Ver `Mi-web/assets/testimonios/README.md`. El modal está
  preparado y probado con una imagen de prueba inyectada únicamente en el navegador.
  Esa imagen nunca se guarda o presenta como un testimonio.

## Validación

El repositorio no contiene scripts de build, lint, typecheck ni una suite previa.
Se añadió una comprobación de navegador reproducible que usa Python Playwright
y Chromium disponibles en el entorno:

```sh
node --check Mi-web/config.js
node --check Mi-web/script.js
python3 tools/check_landing.py --screenshots /tmp/recodifica-review
git diff --check
```

El script inicia y cierra su propio servidor temporal. Comprueba contenido y
precios, destinos de enlaces, formato 16:9, carga única del embed y su estado de
fallo, navegación al video, FAQ exclusivo, detalle VIP por teclado y carrusel
manual en 360, 390, 768, 1440, 767 y 1024 px. También comprueba movimiento reducido,
la página sin JavaScript y el modal (foco, cierre y retorno al disparador).
Las solicitudes a Wistia se bloquean deliberadamente en esta suite para probar
el fallo de red; esto no valida reproducción real. Las capturas y resultados se
guardan fuera del repositorio.

Resultado de esta revisión: los seis escenarios responsive y los tres escenarios
adicionales (movimiento reducido, sin JavaScript y modal con recurso de prueba)
pasaron. También se comprobó un gesto táctil real en Chromium móvil a 390 px:
el carrusel avanzó del primer al segundo testimonio. No se registraron excepciones
de JavaScript en las comprobaciones de la landing. Las capturas de los cuatro
anchos solicitados están en `/workspace/recodifica-review/`.

Antes de publicar: revisar visualmente móvil y escritorio, incorporar los cinco
originales, comprobar la reproducción real y confirmar los importes/destinos de
los checkouts. No hay una URL de preview remota generada por este trabajo.

## Recursos optimizados

Las fotografías originales se conservan sin cambios. Ambas eran PNG aunque sus
nombres terminaban en `.jpg`. Las versiones WebP nuevas pesan 88.050 bytes (hero,
1122 × 1402) y 32.020 bytes (mentor, 720 × 900), frente a 3.853.351 bytes originales
en conjunto. El hero tiene prioridad de carga y el mentor carga diferida.

Montserrat se sirve localmente como WOFF2 variable latino (regular e itálica),
con `font-display: swap`. Fuente: `@fontsource-variable/montserrat@5.3.0`, obtenida
del registro npm. El archivo descargado se verificó con el SHA-512 publicado:

```text
sha512-7PaZoxaxrWLAyrhO46v65An9LhUhfkTExWLhfbywYZCnZEgg/W1rEHnlNmZKjNZ3nJTVYyicqxlJt10z/26yTA==
```

Licencia OFL incluida en `Mi-web/assets/fonts/LICENSE`. No se añadieron paquetes
al proyecto, píxeles, trackers ni un SDK de pago.
