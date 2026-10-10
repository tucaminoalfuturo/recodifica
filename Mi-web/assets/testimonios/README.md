# Capturas originales integradas

Correspondencia verificada visualmente, sin discrepancias de contenido. Los
archivos proporcionados tienen extensión real `.jpg` y se conservan intactos.

| Archivo | Categoría | Dimensiones originales |
| --- | --- | --- |
| `testimonio-1.jpg` | Transformación profunda | 833 × 1449 |
| `testimonio-2.jpg` | Reconexión personal | 705 × 459 |
| `testimonio-3.jpg` | Amor y compasión | 825 × 865 |
| `testimonio-4.jpg` | Transformación familiar | 800 × 742 |
| `testimonio-5.jpg` | Impacto de un video | 800 × 390 |

Los extractos exactos permanecen en `index.html`. El quinto mensaje se identifica
como reacción a un video, no como finalización del entrenamiento de 30 días.
No se añadió la captura del programa de 90 días ni se recrearon mensajes.

`config.js` contiene las rutas y dimensiones reales. `redactions` oculta el área
del autor de la segunda captura (ya tachada en el archivo original). `displayHeight`
deja fuera únicamente la franja de reacciones con iniciales de la tercera y
cuarta captura. Estas medidas se aplican al thumbnail, al modal y a la lectura
sin JavaScript. Ninguna línea del mensaje se recorta. Los archivos originales
subidos por el usuario no se sobrescriben ni eliminan.

La presentación mantiene proporciones, previews compactos y un modal con scroll,
zoom, Escape y retorno del foco. El fallback nativo usa `details`, para permitir
la lectura del mensaje completo cuando JavaScript esté deshabilitado o falle.
Si cambian las imágenes, sincronizar los datos y máscaras de `config.js` con los
fallbacks HTML de `index.html` y verificar visualmente que no haya datos identificables.
