# FloodRisk

Prototipo académico de un dashboard de predicción anual por condado de Estados Unidos.

Proyecto compartido por las materias **Fundamentos de IA** y **Formulación de Proyectos**. Cada materia tiene requisitos y entregables propios; el código y la interfaz son compartidos.

## Estado actual

React, TypeScript y Vite; API FastAPI con SQLite; notebook de entrenamiento en Colab e importador de sus resultados. **El experimento entrenado estima eventos relacionados con inundaciones, no exclusivamente inundaciones.** Las predicciones son experimentales y tienen cobertura limitada. La demo ficticia sigue disponible solo en modo explícito; no sustituye fallos de API.

Al 17 de octubre de 2026, `experimental-v2-geo` está activa en la instalación local: 2,866 predicciones para 2027, antecedentes hasta 2025 y política geográfica explícita. El código no incluye las bases ni los artefactos entrenados; una instalación nueva requiere generarlos/importarlos y activar la versión según las instrucciones siguientes.

Documentación vigente (22 de octubre de 2026): [Fundamentos de IA](docs/FloodRisk_Fundamentos_IA_actualizado.pdf), [Formulación de Proyectos](docs/FloodRisk_Formulacion_actualizada.pdf) e [informe técnico compartido v4](docs/FloodRisk_Informe_v4.pdf). Fuentes editables: [IA](docs/fundamentos_ia_actualizado.md), [Formulación](docs/formulacion_actualizada.md) y [v4](docs/informe_v4.md). El informe v3 se conserva como antecedente. La adaptación móvil modifica presentación y aceptación, no el modelo ni sus probabilidades.

Los documentos específicos reemplazan las propuestas técnicas que ya no corresponden al prototipo; no acreditan aceptación docente. Los resultados de compatibilidad se registran en [la matriz](docs/compatibilidad.md); las pruebas de software no demuestran validez predictiva.

## Prototipo navegable e interfaz

[Abrir el recorrido en Figma](https://www.figma.com/proto/CDXLWi9tsG9jdzsIWuZ3eV?node-id=18-17&starting-point-node-id=18%3A17&scaling=scale-down-width). Usa pantallas y mapas editables con ejemplos de la versión 2: Texas (Harris, Travis y Brooks sin predicción) y Florida (Miami-Dade y Orange). La aplicación web dispone del catálogo completo; el recorrido Figma simula estos cinco casos.

El menú tiene solo **Resumen general** y **Metodología**. El resumen reúne mapa, filtros, resultado e historial. En la vista estatal, los controles **Volver al país**, **Ver estado** y **Acercar selección** se agrupan dentro del encabezado del mapa. Se comprobaron la navegación del prototipo, los filtros y el caso sin resultado; la aceptación final del equipo, la comparación visual completa y la reproducción en otro equipo siguen pendientes. El informe v4 y los documentos por materia reflejan esta evolución; las contribuciones individuales y la aceptación académica siguen pendientes.

## Móvil primero y navegadores

[Recorrido móvil en el mismo archivo Figma](https://www.figma.com/proto/CDXLWi9tsG9jdzsIWuZ3eV?node-id=57-4178&starting-point-node-id=57%3A4178&scaling=scale-down). Doce pantallas de 390 × 844 px y tres filtros superpuestos conservan los casos TX/FL, metodología y navegación, con capas y mapas editables. El recorrido de escritorio conserva su inicio 18:17.

La web usa CSS base móvil y amplía su distribución para tablet/escritorio. Los controles principales tienen al menos 44 px y los selectores 48 px con texto de 16 px. El historial se desplaza dentro de su panel; el resto de la página debe caber desde 320 px. Los filtros permiten seleccionar áreas difíciles de tocar en el mapa.

Para probar desde un teléfono en la misma red, inicia la API en el equipo (puerto 8000) y desde `web` usa `npm run dev -- --host 0.0.0.0`. Abre en el teléfono la IP local del equipo con el puerto anunciado por Vite. No abras localhost en el teléfono para consultar la API del equipo. La web usa `/api` mediante el proxy de `vite.config.ts`; elimina o ajusta cualquier `.env.local` antiguo que apunte a localhost. Si tu API usa 8001, cambia los destinos del proxy en esa configuración. En producción se requiere un proxy equivalente o una URL explícita de API con orígenes autorizados.

El objetivo de sintaxis es Chrome/Edge 107+, Firefox 104+ y Safari 16+; no acredita pruebas en todas esas versiones mínimas. La [matriz de compatibilidad](docs/compatibilidad.md) identifica las versiones ejecutadas. WebKit automatizado no sustituye Safari real de iPhone/Mac, cuya validación permanece pendiente.

Para repetir la prueba funcional con datos v2, inicia API en 8000 y web en 5185 (`npm run dev -- --port 5185 --strictPort`), y en otra terminal desde `web`:

```powershell
npx playwright install chromium firefox webkit
npm run test:browsers
```

La prueba consulta datos reales locales, no usa datos demo y no entrena. Comprueba cuatro anchuras, los cinco casos, navegación, mapa, historial, giro y error de API. Evidencias en `docs/evidence/mobile/`; el informe de resultados registra las versiones. `FLOODRISK_WEB_URL` permite otra dirección de la web.

## Regenerar documentación

Requiere Python y ReportLab. Desde la raíz:

```powershell
python docs/update_mobile_report.py
python docs/build_report.py --source docs/fundamentos_ia_actualizado.md --output docs/FloodRisk_Fundamentos_IA_actualizado.pdf --label "Fundamentos de IA" --date "22 de octubre de 2026"
python docs/build_report.py --source docs/formulacion_actualizada.md --output docs/FloodRisk_Formulacion_actualizada.pdf --label "Formulación de Proyectos" --date "22 de octubre de 2026"
python docs/build_report.py --source docs/informe_v4.md --output docs/FloodRisk_Informe_v4.pdf --label "Informe compartido v4" --date "22 de octubre de 2026"
```

## Abrir en Visual Studio Code

Abre esta carpeta o ejecuta `code .` desde ella. No hace falta conectar el editor a un servicio.

## Ejecutar la interfaz

Requisitos: Node.js 22.12 o superior y npm.

```powershell
cd web
npm install
npm run dev
```

Abre la dirección que indique Vite (normalmente http://localhost:5173; si está ocupada puede ser 5174). Por defecto consulta la API y requiere resultados importados. `npm run build` comprueba TypeScript y genera la versión de producción.

## Ejecutar la API

En otra terminal, desde la raíz del proyecto (Python 3.11 o superior):

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r api/requirements.txt
.\.venv\Scripts\python.exe -m uvicorn api.app.main:app --reload
```

Documentación: http://localhost:8000/docs. SQLite se crea en `storage/floodrisk.db`. La importación de demostración es explícita; iniciar el servidor no inventa ni importa predicciones. Sin importación, las consultas de predicción devuelven 404.

La web usa `VITE_DATA_MODE=api` por defecto. `web/.env.example` documenta la configuración; un archivo local `web/.env.local` puede ajustarla. Reinicia Vite después de cambiar variables. Para ver exclusivamente ejemplos sin API, establece explícitamente `VITE_DATA_MODE=mock`.

En esta instalación local se configuró `VITE_API_URL=http://127.0.0.1:8001/api` porque el puerto 8000 ya ejecutaba una API anterior. Para conservar esa configuración, inicia la API con `.\.venv\Scripts\python.exe -m uvicorn api.app.main:app --reload --port 8001`. También puedes detener tú la instancia anterior y volver a configurar ambos lados en 8000; los puertos de web y API son independientes.

## Importar resultados de Colab

Desde la raíz del proyecto, antes de consultar resultados, ejecuta (ajusta las rutas a tus archivos):

```powershell
.\.venv\Scripts\python.exe -m api.scripts.import_colab --zip "C:\Users\Alejandro\Documents\floodrisk_modelo_v1.zip" --dataset-zip "C:\Users\Alejandro\Downloads\Riesgo de inundaciones para seguros en USA (1).zip"
```

El primer ZIP contiene `predicciones.csv` y `metadatos.json`; el segundo es el ZIP original exacto utilizado en Colab. Se verifica su hash y se importan conteos históricos NOAA hasta el corte. El historial no se reconstruye con etiquetas binarias. `--dataset-zip` es opcional: sin él solo se cargan predicciones y la web no muestra historial ficticio para resultados entrenados.

La importación valida claves, probabilidades, corte, desfase y metadatos antes de escribir, y crea un respaldo `storage/floodrisk.before-colab-*.db`. Reimportar la misma versión actualiza sus resultados, sin duplicarlos. Nunca se carga ni ejecuta `modelo.joblib`; el dashboard consulta predicciones precalculadas. No hace falta instalar scikit-learn en la API.

Con resultados entrenados para un año, la API excluye predicciones demo de ese año. Si un condado no tiene resultado entrenado, devuelve 404 y la interfaz muestra “Sin predicción disponible”; nunca un 0 % inventado. La consulta de historial incluye `is_demo=false` para evitar mezclar fuentes.

El catálogo geográfico identifica nombres con coincidencia exacta de FIPS. Los códigos que no coinciden se muestran “Código XXXXX sin validar”; no se inventa una ubicación. La última versión se selecciona por fecha de generación, después de aplicar la separación demo/entrenado.

## Mapa interactivo y catálogo

## Activación de versiones

`active_versions` fija una versión completa por año objetivo. Tarjetas y mapas consultan exclusivamente esa versión; un código ausente no se completa con v1 ni con demo. Si todavía no hay activación explícita, la compatibilidad elige una versión global por año, no una por condado.

Tras importar el ZIP en la base deseada, activar su versión/política con:

```powershell
.\.venv\Scripts\python.exe -m api.scripts.activate_version --zip "ruta\floodrisk_modelo_v2.zip"
```

El comando comprueba que los valores importados coincidan exactamente con el paquete y que la emisión respete la política, crea un respaldo y registra versión/política en una transacción. No ejecuta joblib. Los registros de otras versiones se conservan.

La instalación local utiliza `storage/active_database.json` (excluido de Git) con `database: storage/floodrisk-v2-staged.db`. La base `storage/floodrisk.db` anterior permanece intacta. `FLOODRISK_DB`, si está definido, tiene prioridad sobre el archivo local. Sin ambos, se usa `storage/floodrisk.db`. La base preparada contiene tanto v1 como v2 y activa `experimental-v2-geo` para 2027.

El historial solicita año objetivo y versión; omite códigos fuera del catálogo de la política y filas en cuarentena, sin borrar los originales. Si la versión cambia entre consultas, devuelve 409 para solicitar una nueva carga. Este filtrado no implica que todos los eventos históricos hayan sido auditados. `/health` informa las versiones activas.

Para volver a la instalación previa, cambia el archivo local a `storage/floodrisk.db` y reinicia la API (sin una variable de entorno que lo anule). Esto revierte la conexión sin eliminar ni sobrescribir ninguna base. No cambies solo la fecha de generación para forzar una versión.

### Geografía

Leaflet muestra límites vectoriales oficiales del Census de 2025, sin depender de teselas de terceros. Los filtros y el clic en un condado comparten la selección. Hay zoom, controles para ver el estado/acercar selección, leyenda de intervalos probabilísticos y gris para áreas sin predicción (nunca se interpreta como cero). El mapa sigue visible cuando se selecciona un área sin resultado.

La vista inicial es nacional, dividida por estados. Un clic en un estado abre sus condados y actualiza los filtros. El botón “Volver a Estados Unidos” regresa a la vista nacional. Alaska y Hawaii aparecen reubicados como insets a distinta escala para conservar la silueta reconocible del país; al abrirlos se muestran sus límites geográficos sin esa reubicación. Los colores nacionales solo identifican estados y selección, no probabilidades estatales agregadas. `/api/states` sirve los límites estatales originales.

Para regenerar el catálogo en una instalación nueva:

```powershell
.\.venv\Scripts\python.exe -m pip install -r api/requirements-geography.txt
.\.venv\Scripts\python.exe -m api.scripts.prepare_geography
```

Requiere Internet solo durante la preparación. Reinicia la API tras regenerar límites para renovar la caché. Los archivos generados son locales en `data/geographic/` y no se versionan; su README documenta la procedencia. La preparación amplía el catálogo incluso con áreas sin predicción y actualiza nombres en SQLite sin modificar porcentajes.

**Antecedente de v1, tratado por la política v2 descrita arriba:** 66 códigos del export no coinciden con los catálogos de 2020/2025 y ocho códigos históricos de Connecticut no tienen límites actuales coincidentes. Los registros originales se conservan; en la emisión activa v2 se excluyen esos códigos y los 48 pares Georgia/2025 en cuarentena. No se redistribuyen sus probabilidades. Revisar la geocodificación de los datos de origen antes del siguiente entrenamiento. Los conteos de cobertura del mapa se refieren a coincidencias exactas, no a validación integral del dataset.

El resultado inicial de Colab contiene 2,988 predicciones de 2027 con antecedentes hasta 2025. `/health` muestra `experimental_predictions_loaded` cuando existen resultados entrenados. Estos datos locales y respaldos SQLite no se incluyen en Git.

## Carpetas

- `data/raw/`: originales locales, sin modificar. Los archivos sincronizados del proyecto ChatGPT no se mueven ni se editan.
- `data/processed/`: tablas derivadas; `data/geographic/`: GeoJSON; `data/demo/`: ejemplos ficticios versionados.
- `ml/notebooks/`: experimentación en Colab; `ml/src/`: preparación, variables, entrenamiento, evaluación y predicción.
- `ml/artifacts/`: modelos y metadatos; `ml/reports/`: evaluaciones.
- `api/`: servicio y carga de resultados; `web/`: interfaz; `storage/`: SQLite local.
- `tests/`: contratos de datos y validación del corte temporal.

## Contrato de predicción

Una predicción identifica `county_fips`, `target_year`, `probability`, `data_cutoff`, `generated_at`, `model_version` e `is_demo`, junto con `is_experimental`, `event_definition`, `horizon_years`, `input_snapshot_at` y `limitations`. `probability` está entre 0 y 1; FIPS conserva cinco caracteres. La etiqueta inicial es `flood_related_event_count > 0`, que agrupa inundaciones, lluvia fuerte, huracanes y marejadas según el diccionario. Los reclamos NFIP no equivalen a todos los eventos de inundación. No se inventan factores individuales: este export no los contiene.

Cada variable debe usar únicamente información disponible en la fecha de corte y el corte debe ser anterior al 1 de enero del año objetivo. También se debe registrar la disponibilidad/publicación de los datos. La validación se separará por años completos, con todos los condados de un año en el mismo grupo. Las transformaciones y la calibración se ajustarán sin observar el conjunto de evaluación final.

La demo de 2027 utiliza un corte ilustrativo de 2025-12-31. No presupone que 2026 esté completo. Los ejemplos no proceden de los datasets del proyecto.

## Comprobaciones

```powershell
.\.venv\Scripts\python.exe -m pip install -r api/requirements-dev.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
cd web
npm run build
```

## Próximo trabajo

1. Validar catálogo FIPS, cobertura y retrasos de publicación; decidir si obtener etiquetas específicas de inundación.
2. Revisar calibración y resultados del experimento; no confundir ROC-AUC con exactitud.
3. Investigar códigos sin correspondencia y posibles zonas meteorológicas antes de reentrenar; el mapa no los remapea.
4. Recopilar evidencias de la interfaz y aportaciones para ambas materias.

No se incluyen autenticación, despliegue ni LM Studio en esta primera estructura.
