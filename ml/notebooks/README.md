# Notebooks de Colab

Guardar aquí exploración, auditoría y experimentos. Pasar el código reutilizable a `ml/src/`. Ajustar transformaciones y calibración solamente sobre los periodos permitidos; reservar el último año completo para evaluación final.

## Primera versión de entrenamiento

`02_entrenamiento_floodrisk.ipynb` se abre en Google Colab con CPU. Ejecutar en orden y subir el ZIP original de datasets cuando lo solicite. No requiere GPU, LM Studio ni claves.

- Predice presencia anual de eventos NOAA relacionados con inundaciones (definición amplia del diccionario, no exclusivamente Flood/Flash Flood).
- Objetivo inicial: 2027 con antecedentes hasta 2025, manteniendo el mismo desfase de dos años en los ejemplos históricos.
- Entrenamiento hasta 2022, selección en 2023 y prueba en 2024–2025. Después reentrena con etiquetas hasta 2025.
- Compara referencia constante, regresión logística y árboles potenciados. No presupone que el modelo complejo gane.
- Exporta predicciones, tabla preparada, métricas, modelo y metadatos en un ZIP descargable. La integración con API/dashboard sigue pendiente.

Las ausencias NOAA no se convierten en negativos. La población evaluada depende de filas NOAA disponibles y no representa cobertura validada de todos los condados. Consultar las limitaciones del notebook antes de interpretar porcentajes. Los datos revisados en 2026 tampoco permiten reproducir exactamente la disponibilidad de publicaciones históricas.
