# FloodRisk

Prototipo académico de un dashboard de predicción anual por condado de Estados Unidos.

Proyecto compartido por las materias **Fundamentos de IA** y **Formulación de Proyectos**. Cada materia tiene requisitos y entregables propios; el código y la interfaz son compartidos.

## Estado actual

Estructura inicial con React, TypeScript y Vite; API FastAPI con SQLite; datos ficticios compartidos y módulos de aprendizaje automático pendientes de implementar. **No hay un modelo entrenado. Todas las probabilidades y los historiales de demostración son ficticios.**

## Abrir en Visual Studio Code

Abre esta carpeta o ejecuta `code .` desde ella. No hace falta conectar el editor a un servicio.

## Ejecutar la interfaz

Requisitos: Node.js 22.12 o superior y npm.

```powershell
cd web
npm install
npm run dev
```

Abre http://localhost:5173. Por defecto utiliza los datos de ejemplo, sin necesitar la API. `npm run build` comprueba TypeScript y genera la versión de producción.

## Ejecutar la API

En otra terminal, desde la raíz del proyecto (Python 3.11 o superior):

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r api/requirements.txt
.\.venv\Scripts\python.exe -m api.scripts.import_predictions --demo
.\.venv\Scripts\python.exe -m uvicorn api.app.main:app --reload
```

Documentación: http://localhost:8000/docs. SQLite se crea en `storage/floodrisk.db`. La importación de demostración es explícita; iniciar el servidor no inventa ni importa predicciones. Sin importación, las consultas de predicción devuelven 404.

Para conectar la web, copia `web/.env.example` a `web/.env.local`, cambia `VITE_DATA_MODE=api` y reinicia Vite. En modo API los errores se muestran, sin sustituirlos silenciosamente por ejemplos.

## Carpetas

- `data/raw/`: originales locales, sin modificar. Los archivos sincronizados del proyecto ChatGPT no se mueven ni se editan.
- `data/processed/`: tablas derivadas; `data/geographic/`: GeoJSON; `data/demo/`: ejemplos ficticios versionados.
- `ml/notebooks/`: experimentación en Colab; `ml/src/`: preparación, variables, entrenamiento, evaluación y predicción.
- `ml/artifacts/`: modelos y metadatos; `ml/reports/`: evaluaciones.
- `api/`: servicio y carga de resultados; `web/`: interfaz; `storage/`: SQLite local.
- `tests/`: contratos de datos y validación del corte temporal.

## Contrato de predicción

Una predicción identifica `county_fips`, `target_year`, `probability`, `data_cutoff`, `generated_at`, `model_version` e `is_demo`. `probability` está entre 0 y 1; FIPS conserva cinco caracteres. El objetivo propuesto es al menos una inundación reportada durante el año objetivo, pendiente de construir etiquetas específicas de inundación con NOAA. Los reclamos NFIP no se interpretan como si fueran todos los eventos de inundación.

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

1. Auditar datasets y definir etiquetas NOAA específicas, cobertura y retrasos de publicación.
2. Construir variables históricas, baseline y evaluación temporal en Colab.
3. Entrenar y calibrar el modelo, guardar métricas y metadatos reproducibles.
4. Añadir GeoJSON y mapa interactivo, y cargar resultados reales con un contrato validado.

No se incluyen autenticación, despliegue ni LM Studio en esta primera estructura.
