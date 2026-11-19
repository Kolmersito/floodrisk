FloodRisk
Dashboard académico de riesgo anual por condado de Estados Unidos, con React y FastAPI. Las predicciones son experimentales y estiman eventos relacionados con inundaciones.
Requisitos
- Git, Python 3.11 o superior y Node.js 22.12 o superior (con npm).
- Internet para instalar dependencias y descargar los límites del mapa.
- El ZIP original del dataset para entrenar, o un ZIP de resultados ya entrenados para importar.
Los comandos siguientes son para Windows PowerShell.
1. Descargar el repositorio
git clone https://github.com/Kolmersito/floodrisk.git
cd floodrisk
2. Preparar y ejecutar la API
Desde la raíz del proyecto:
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r api/requirements.txt -r api/requirements-geography.txt -r ml/requirements.txt
.\.venv\Scripts\python.exe -m api.scripts.prepare_geography
.\.venv\Scripts\python.exe -m uvicorn api.app.main:app
Deja esta terminal abierta. Documentación de la API: http://localhost:8000/docs.
3. Ejecutar la web
En otra terminal, desde la raíz del proyecto:
cd web
Copy-Item .env.example .env.local
npm ci
npm run dev
Abre la dirección que indique Vite, normalmente http://localhost:5173.
4. Cargar predicciones
Git no incluye datasets, modelos entrenados ni bases SQLite. Elige una opción:

Entrenar desde la web: abre Entrenamiento, sube el ZIP original del dataset (máximo 50 MB), espera a que termine y pulsa Usar estos resultados en el mapa. Mantén una sola instancia de la API abierta durante el proceso.

Importar resultados existentes: desde la raíz, en otra terminal, sustituye las rutas de ejemplo:
.\.venv\Scripts\python.exe -m api.scripts.import_colab --zip "C:\ruta\resultados.zip" --dataset-zip "C:\ruta\dataset-original.zip"
.\.venv\Scripts\python.exe -m api.scripts.activate_version --zip "C:\ruta\resultados.zip"
El ZIP de resultados debe incluir predicciones.csv y metadatos.json. El ZIP original permite cargar el historial; puedes omitir --dataset-zip si solo necesitas predicciones. Actualiza la web al terminar. Los condados sin resultados mostrarán Sin predicción disponible.
Volver a abrir el proyecto
Solo necesitas iniciar la API (último comando del paso 2) y ejecutar npm run dev dentro de web. La base se guarda en storage/floodrisk.db por defecto.

Si cambias el puerto de la API, ajusta VITE_API_URL en web/.env.local y reinicia Vite. En Linux/macOS usa python3 para crear el entorno, .venv/bin/python en lugar de .\.venv\Scripts\python.exe y cp .env.example .env.local para copiar la configuración.
