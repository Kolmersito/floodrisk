# Verificación móvil y compatibilidad

Actualización: 22 de octubre de 2026. Producto: FloodRisk, una aplicación web adaptable.

## Alcance

CSS base móvil; ampliaciones desde 621, 1001 y 1280 px. Controles principales de al menos 44 px; selectores de 48 px y fuente de 16 px. La página debe conservar el contenido a 320 px; el historial conserva su desplazamiento dentro del panel. El mapa permite selección alternativa por filtros.

La compilación fija Chrome/Edge 107, Firefox 104 y Safari 16 como referencia de sintaxis. No significa que esas versiones mínimas hayan sido probadas. Solo las ejecuciones de la matriz cuentan como evidencia.

## Ejecución reproducible

Con la base activa y geografía preparadas según README, iniciar la API en 127.0.0.1:8000 y la web en 127.0.0.1:5185. Desde web, instalar dependencias con npm ci, preparar motores con npx playwright install chromium firefox webkit y ejecutar npm run test:browsers. FLOODRISK_WEB_URL permite otra dirección de la web.

La prueba usa la API real de v2, no respuestas ficticias: Harris, Travis, Brooks sin resultado, Miami-Dade y Orange; filtros, acercamiento, regreso al país, metodología, historial, giro de pantalla, fallo de API y ausencia de excepciones no controladas. Se comprueba desbordamiento en todas las anchuras. No es una auditoría de accesibilidad completa ni una prueba de carga.

Las ejecuciones producen docs/evidence/mobile/results.json, una captura Chromium de escritorio y una WebKit móvil. El archivo de resultados conserva las versiones y la marca de tiempo UTC; los informes usan la fecha local de Cancún.

## Matriz y estado

| Motor automatizado | Versión ejecutada | Anchuras (px) | Resultado |
| --- | --- | --- | --- |
| chromium | 151.0.7922.34 | 320, 390, 768, 1440 | 4 recorridos aprobados |
| firefox | 153.0 | 320, 390, 768, 1440 | 4 recorridos aprobados |
| webkit | 26.5 | 320, 390, 768, 1440 | 4 recorridos aprobados |

Doce combinaciones aprobadas contra una copia local de experimental-v2-geo. Giro 390 x 844 a 844 x 390 comprobado en los tres motores. Compilación TypeScript/Vite correcta. Fecha UTC de la ejecución: 2026-10-23T02:18:29.626Z.

Durante la primera ejecución WebKit detectó una excepción de Leaflet al navegar mientras una animación seguía activa. Se desactivaron las animaciones de zoom/transición, se fijó animate:false en los ajustes de límites y se detiene el mapa antes de retirarlo. La repetición completa pasó sin excepciones no controladas. Los gestos y controles de zoom permanecen disponibles.

Safari real de iPhone y macOS: pendiente. WebKit de Playwright es un motor de pruebas relacionado, no el navegador Safari instalado. Chrome real de Android, Edge real, dispositivos físicos y versiones mínimas: pendientes; tampoco se acreditan por la emulación de un ancho de pantalla.

## Prueba manual con teléfono

En la misma red, iniciar la API en el equipo y ejecutar desde web: npm run dev -- --host 0.0.0.0. Abrir desde el teléfono http://IP-LOCAL-DEL-EQUIPO:5173 (o el puerto anunciado). El proxy /api dirige las consultas a 127.0.0.1:8000 en el equipo. Si la API usa otro puerto, cambiar ambos destinos de proxy en web/vite.config.ts.

Usar VITE_API_URL=/api o eliminar una configuración local antigua que apunte a localhost. En el teléfono localhost identifica al propio teléfono. La conexión depende de que la red y las reglas de acceso del equipo permitan el puerto. Esta guía no configura ni publica un servicio en Internet.

En producción, servir /api desde el mismo dominio mediante un proxy equivalente o definir una URL de API y configurar sus orígenes autorizados. vite preview se usa para revisar la compilación local, no como servidor de producción.

## Referencias

https://v7.vite.dev/guide/build ; https://vite.dev/config/server-options.html#server-proxy ; https://playwright.dev/docs/browsers . Requisitos docentes: apuntes de clase y aclaración oral del estudiante; rúbrica escrita y versiones exigidas por confirmar.
