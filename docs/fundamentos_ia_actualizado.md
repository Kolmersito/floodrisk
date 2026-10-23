# FloodRisk: diseño actualizado del proyecto de inteligencia artificial

Universidad Tecnológica de Cancún. Ingeniería en Tecnologías de la Información e Innovación Digital. Grupo LITIID 72.

Materia: Fundamentos de Inteligencia Artificial. Actualización técnica del 22 de octubre de 2026. Equipo: Jade Alejandro Morales Millan; Roberto Pablo Angeles García; Kristopher Eiael Cortez Vargas; José Antonio Navarro Galván. Contribuciones individuales por confirmar con el equipo.

## 1. Descripción del problema y alcance

FloodRisk es un prototipo académico para explorar antecedentes por condado de Estados Unidos y consultar una estimación anual experimental de la presencia de al menos un evento NOAA relacionado con inundaciones. Unifica la consulta de fuentes históricas y presenta sus limitaciones de forma visible en móvil y escritorio.

El problema implementado es clasificación binaria supervisada sobre datos tabulares por condado-año: flood_related_event_count > 0. La etiqueta incluye inundaciones, lluvia fuerte, huracanes y marejadas según el diccionario del paquete; no es una etiqueta exclusiva de inundación. Las ausencias de observaciones no se convierten automáticamente en cero eventos.

El usuario consulta año, estado y condado, revisa probabilidad, corte temporal, versión y antecedentes. El sistema sirve para una demostración y exploración académica. No calcula pérdidas futuras, primas de seguros, evacuaciones ni alertas meteorológicas.

Esta revisión sustituye el alcance técnico del diseño original con base en el informe v3 y el código, sin acreditar aprobación docente ni cambiar la rúbrica.

| Diseño original | Alcance implementado |
| --- | --- |
| LightGBM para pérdidas y reclamaciones severas | Regresión logística para presencia de eventos relacionados |
| Ranking de pérdidas futuras | Consulta de probabilidad experimental por condado |
| Explicaciones SHAP individuales | No calculadas; la interfaz comunica su ausencia |
| Metas de AUC y captura de pérdidas | Métricas retrospectivas observadas, sin prometer umbrales |
| Tablero en nube y acceso por roles | Aplicación local; despliegue y autenticación fuera del alcance actual |

## 2. Metodología y justificación

Se sigue un proceso iterativo compatible con CRISP-DM: comprender el problema, auditar y preparar datos, comparar modelos, evaluar y presentar resultados. Se aprende de tablas etiquetadas, sin un modelo de lenguaje.

Se compararon referencia constante, regresión logística y HistGradientBoostingClassifier, con semilla 42. La logística fue seleccionada por menor Brier en validación de 2023. La versión v1 se ejecutó en Colab; v2 se ejecutó localmente y tiene notebook preparado para Colab. No se afirma una nueva ejecución de v2 en Colab.

Cada ejemplo usa el año base y sus dos años calendario anteriores. El objetivo corresponde a dos años después del año base. Para emitir 2027 se utilizan antecedentes de 2025, 2024 y 2023. El año parcial 2026 se excluye. Imputación, escalado y codificación se ajustan dentro del pipeline de entrenamiento.

| Etapa | Años objetivo | Uso |
| --- | --- | --- |
| Entrenamiento | 2005 a 2022 | Ajustar parámetros y transformaciones |
| Validación | 2023 | Selección por Brier |
| Evaluación retrospectiva | 2024 y 2025 | Comparar modelos antes del reajuste |
| Reajuste final | Etiquetas hasta 2025 | Emisión experimental para 2027 |

La instantánea fue generada en agosto de 2026 y contiene revisiones históricas. No reproduce exactamente lo disponible en cada fecha pasada. Los años de evaluación ya se habían observado durante el trabajo anterior; la comparación v2 no es una prueba independiente nueva.

## 3. Datos y preparación

El paquete contiene 80,419 filas de eventos NOAA, 33,098 de reclamaciones NFIP, 31,280 de declaratorias FEMA y 83,804 de tabla integrada. Las fuentes no representan cobertura universal ni tienen equivalencia semántica: una reclamación no es un evento meteorológico.

Se conservan FIPS como cinco caracteres y se emplean uniones de años exactos. La auditoría identificó 50,707 faltantes en paid_loss_to_claim_coverage y flood_zone_count constante en cero. Esas columnas no se añaden indiscriminadamente al modelo. Los originales se mantienen sin modificación.

La política geo-quarantine-v2 exige coincidencia con Census 2025 y excluye 48 pares de Georgia en 2025 por nombre incompatible. Respecto a la emisión v1, se retiran 66 códigos sin correspondencia, ocho históricos de Connecticut y esos 48 pares: 122 códigos en total. No se redistribuyen eventos ni probabilidades por semejanza de nombres.

V2 usa 59,520 ejemplos supervisados y emite 2,866 resultados para 2027 sobre 3,144 áreas actuales. Las 278 áreas restantes se muestran sin resultado. La revisión de eventos individuales cubrió 2025, no toda la serie histórica.

## 4. Diseño de la solución e interfaz móvil

Flujo: fuentes originales, preparación en Python, entrenamiento fuera de la web, exportación CSV/JSON, importación validada en SQLite, consulta por FastAPI y presentación en React con TypeScript/Vite. Leaflet representa límites vectoriales. La API sirve probabilidades precalculadas y no ejecuta archivos joblib.

Se utiliza una sola aplicación web adaptable. El diseño comienza en móvil y amplía su distribución para escritorio. El navegador no vuelve a entrenar el modelo; cambiar el ancho de pantalla no modifica las probabilidades, la versión, la cobertura ni el corte temporal.

El recorrido principal es país, estado, condado y resultado. Se combina una jerarquía geográfica con vistas filtradas por año y territorio y tarjetas de resumen. Figma representa cinco casos en Texas y Florida; la web consulta el catálogo completo disponible. El prototipo no está conectado en vivo a la API.

Los selectores tienen 16 px y altura mínima de 48 px; botones de navegación y acciones, al menos 44 px. El historial puede desplazarse horizontalmente dentro de su panel. El contenido general debe mantenerse legible a partir de 320 px, sin desbordamiento lateral de la página. La selección por filtros es una alternativa al toque de polígonos pequeños del mapa.

En desarrollo se consulta /api en el mismo origen mediante el proxy de Vite. Así el teléfono no intenta conectarse a su propio localhost. En un despliegue debe existir un servicio equivalente para /api o una URL explícita autorizada con su configuración de acceso correspondiente.

## 5. Evaluación de IA y de software

La comparación siguiente procede del informe v3 y usa casos comunes. No corresponde a resultados observados de 2027 ni a un nuevo entrenamiento motivado por el diseño móvil.

| Año / casos | Modelo v2 | ROC-AUC | Brier | Average precision |
| --- | --- | ---: | ---: | ---: |
| 2024 / 2,815 | Regresión logística | 0.681422 | 0.224488 | 0.729493 |
| 2025 / 2,772 | Regresión logística | 0.738773 | 0.206989 | 0.777256 |

AUC mide discriminación, no porcentaje de aciertos. Brier evalúa el error de las probabilidades; no se ha aplicado calibración adicional. Average precision no equivale al área trapezoidal bajo la curva precisión-recall. La restricción geográfica de v2 apenas cambia el desempeño respecto a v1.

La verificación de interfaz se registra por separado en docs/compatibilidad.md: navegador y versión, resolución, consulta real, ausencia de resultado, metodología, desplazamiento y cambio de orientación. WebKit automatizado aproxima un entorno relacionado con Safari, pero no sustituye Safari real en iPhone y Mac. Las pruebas visuales y de software no demuestran validez predictiva.

## 6. Conclusiones y trabajo pendiente

El proyecto ya integra un modelo tabular experimental con una web de consulta. La incorporación de móvil cambia la presentación, el acceso y los criterios de aceptación; no justifica sustituir el algoritmo ni repetir el entrenamiento.

Continúan pendientes la auditoría histórica completa, una evaluación futura independiente para cambios de modelado, la calibración de probabilidades, decidir si generar explicaciones individuales, la reproducción por otro integrante y la aceptación académica. Safari real y las contribuciones individuales requieren evidencia específica; no se declaran aprobados por inferencia.

## 7. Referencias y evidencias

Estado técnico y métricas: docs/informe_v3.md, 17 de octubre de 2026; actualización compartida: docs/informe_v4.md. Código y notebooks: https://github.com/Kolmersito/floodrisk. Los datos y modelos locales permanecen fuera de Git.

Prototipo móvil: https://www.figma.com/proto/CDXLWi9tsG9jdzsIWuZ3eV?node-id=57-4178&starting-point-node-id=57%3A4178&scaling=scale-down. Prototipo escritorio: mismo archivo, inicio 18:17.

Material de clase: apuntes FORMULACION en https://app.notion.com/p/4019d94868e680a982d2eeb4cf8cd620 y dos fotos proporcionadas por el estudiante sobre modelos de navegación y reglas UX. La prioridad mobile first y Safari procede de su aclaración de la explicación oral, no de una rúbrica escrita confirmada.

Fuentes de datos: NOAA Storm Events, OpenFEMA (NFIP y declaratorias) y límites Census 2025. Enlaces oficiales y procedencia en el informe v4 y data/geographic/README.md.

Compatibilidad: https://v7.vite.dev/guide/build y https://playwright.dev/docs/browsers . Hashes de geografía en manifiestos locales.
