# Notebooks de Colab

## Versión 2 con restricciones geográficas

`03_entrenamiento_floodrisk_v2_geografia.ipynb` conserva v1 y añade una política incorporada: coincidencia con geometrías Census 2025 y cuarentena de 48 pares código-año de Georgia (2025) con nombre incompatible en NOAA. No reasigna eventos por nombre. Las diferencias de tildes, sufijos y marcadores `(C)` se normalizan para evitar exclusiones por formato.

La política limita el alcance a geografía actual: no afirma que todos los códigos históricos excluidos sean falsos, ni valida toda la serie evento por evento. Exporta política y filas excluidas junto con un modelo `experimental-v2-geo`. Los originales y el dashboard no se modifican al ejecutar el notebook. La comparación en años 2024–2025 es retrospectiva sobre periodos ya utilizados; no es un nuevo test independiente.

Se ejecuta en Colab subiendo el ZIP original; no requiere subir el diagnóstico ni el catálogo por separado. La primera comprobación de v2 se realizó localmente; debe conservarse el registro de versiones del entorno al comparar con resultados de Colab.

Guardar aquí exploración, auditoría y experimentos. Pasar el código reutilizable a `ml/src/`. Ajustar transformaciones y calibración solamente sobre los periodos permitidos; reservar el último año completo para evaluación final.

## Primera versión de entrenamiento

`02_entrenamiento_floodrisk.ipynb` se abre en Google Colab con CPU. Ejecutar en orden y subir el ZIP original de datasets cuando lo solicite. No requiere GPU, LM Studio ni claves.

- Predice presencia anual de eventos NOAA relacionados con inundaciones (definición amplia del diccionario, no exclusivamente Flood/Flash Flood).
- Objetivo inicial: 2027 con antecedentes hasta 2025, manteniendo el mismo desfase de dos años en los ejemplos históricos.
- Entrenamiento hasta 2022, selección en 2023 y prueba en 2024–2025. Después reentrena con etiquetas hasta 2025.
- Compara referencia constante, regresión logística y árboles potenciados. No presupone que el modelo complejo gane.
- Exporta predicciones, tabla preparada, métricas, modelo y metadatos en un ZIP descargable. La integración con API/dashboard está implementada mediante importación y activación explícita; consultar el README principal. La versión activa local es experimental-v2-geo.

Las ausencias NOAA no se convierten en negativos. La población evaluada depende de filas NOAA disponibles y no representa cobertura validada de todos los condados. Consultar las limitaciones del notebook antes de interpretar porcentajes. Los datos revisados en 2026 tampoco permiten reproducir exactamente la disponibilidad de publicaciones históricas.
