# FloodRisk: informe actualizado del prototipo académico

Universidad Tecnológica de Cancún. Ingeniería en Tecnologías de la Información e Innovación Digital. Grupo LITIID 72.

Materias: Fundamentos de IA y Formulación de Proyectos. Informe versión 4, actualizado el 22 de octubre de 2026. Versión del modelo: experimental-v2-geo.

Integrantes: Jade Alejandro Morales Millan; Roberto Pablo Angeles García; Kristopher Eiael Cortez Vargas; José Antonio Navarro Galván. Las aportaciones y responsabilidades individuales deben confirmarse por el equipo.

## 1. Alcance y estado ejecutivo

FloodRisk es un dashboard académico que permite explorar estados y condados de Estados Unidos, consultar antecedentes y mostrar una estimación anual experimental obtenida de patrones históricos. El objetivo implementado es la presencia de al menos un evento NOAA relacionado con inundaciones, según flood_related_event_count > 0. La definición incluye otros fenómenos relacionados; no representa exclusivamente inundaciones confirmadas.

El modelo está entrenado y sus resultados están integrados en la aplicación local. La versión 2 emite 2,866 predicciones para 2027, con antecedentes hasta 2025 y desfase fijo de dos años. El año parcial 2026 no participa. La versión anterior y las bases de respaldo se conservan. No se sustituyen resultados ausentes por probabilidades de otra versión.

La propuesta empresarial anterior se sustituye por un prototipo reproducible. No se prometen AUC de 0.80, pérdidas económicas, primas de seguros ni ahorros financieros. Quedan fuera las alertas diarias, evacuaciones, actualización continua, cuentas de usuarios y chatbot. LM Studio no es necesario para el modelo tabular.

Figma dispone de un recorrido de escritorio y otro móvil de 390 x 844 px en el mismo archivo, con cinco casos TX/FL, filtros, metodología y acercamientos. La comparación visual sistemática y la aceptación académica requieren evidencia adicional. El despliegue público y la reproducción por otro integrante desde una copia limpia todavía no se han acreditado.

## 2. Datos y decisiones de calidad

El paquete original fue generado el 21 de agosto de 2026 y contiene agregados anuales de 2000 a 2026. La fecha de generación no acredita que todas las fuentes estén completas hasta ese día. No contiene la resolución mensual necesaria para aprender específicamente los meses restantes de 2026.

| Fuente o tabla | Filas | Uso |
| --- | ---: | --- |
| Eventos NOAA por condado y año | 80,419 | Eventos históricos y etiqueta amplia |
| Reclamaciones NFIP | 33,098 | Antecedentes de seguros |
| Declaratorias FEMA | 31,280 | Antecedentes de declaratorias |
| Tabla integrada | 83,804 | Cruces y revisión estructural |
| Perfil más reciente | 3,511 | Referencia, no predictores globales futuros |

La auditoría inicial no encontró duplicados condado-año en las cuatro tablas principales. Detectó 225 filas de la integrada con códigos terminados en 000, 50,707 faltantes en paid_loss_to_claim_coverage y flood_zone_count constante en cero. Esas columnas no se incorporan indiscriminadamente al modelo. El ajuste NFIP negativo de 31011 en 2022 se trata como faltante para la variable monetaria y se conserva un indicador; el original no se modifica.

Las ausencias de filas NOAA no se convierten automáticamente en negativos. La evaluación depende de casos con observaciones disponibles en el año base y objetivo. Los reclamos asegurados y las declaratorias no equivalen a cobertura universal de inundaciones. Los importes históricos se expresan en dólares nominales.

## 3. Corrección geográfica de la versión 2

Se contrastaron claves con los catálogos Census 2020 y 2025 y se revisó el archivo original de eventos NOAA de 2025. La geometría actual comprende 3,144 condados o equivalentes en 50 estados y DC. La revisión de eventos individuales cubrió 2025, no toda la serie histórica.

| Exclusión respecto a la emisión v1 | Códigos | Decisión |
| --- | ---: | --- |
| Sin correspondencia en los dos catálogos | 66 | No emitir; investigar origen |
| Condados históricos de Connecticut | 8 | No redistribuir a regiones actuales |
| Pares código-año de Georgia en 2025 | 48 | Cuarentena por nombre incompatible |
| Total sin emisión respecto a v1 | 122 | Conservar originales y trazabilidad |

Los 66 códigos se reparten entre Alaska (17) y Georgia (49). Las discrepancias de Georgia se normalizaron por acentos, sufijos y marcadores antes de confirmar los 48 pares sustantivos. Los conteos de los 66 códigos coincidían con eventos marcados C en la fuente: no se atribuye el problema sin evidencia a una mezcla de zonas Z.

La política geo-quarantine-v2 se aplica antes de construir variables y etiquetas. Exige coincidencia exacta con la geometría actual y elimina los pares en cuarentena. Limitar el alcance a 2025 no significa que todos los códigos históricos excluidos sean falsos. No se reasignan eventos por similitud de nombres.

Los ejemplos supervisados pasan de 59,819 a 59,520; las predicciones de 2,988 a 2,866. Las 2,866 tienen geometría actual; 278 de las 3,144 áreas actuales quedan sin resultado. La auditoría geográfica completa permanece abierta.

## 4. Construcción y evaluación del modelo

Cada ejemplo combina un año base y sus dos años anteriores mediante uniones de años calendario exactos. La etiqueta corresponde a dos años después del año base. Para 2027 se usan antecedentes 2025, 2024 y 2023. Imputación, escalado y codificación del estado se ajustan dentro del pipeline de entrenamiento; los montos usan transformación logarítmica. Se excluyen percentiles globales y perfiles recientes que introducirían información posterior.

| Etapa | Años objetivo | Propósito |
| --- | --- | --- |
| Entrenamiento | 2005 a 2022 | Ajustar modelos y transformaciones |
| Validación | 2023 | Elegir por menor Brier |
| Prueba retrospectiva | 2024 y 2025 | Comparar con la referencia |
| Reajuste final | Etiquetas hasta 2025 | Emitir resultados para 2027 |

Se compararon referencia constante, regresión logística y HistGradientBoostingClassifier, con semilla 42. Ganó la regresión logística por Brier de validación. V1 se ejecutó por el usuario en Colab; v2 se ejecutó y verificó localmente y dispone de notebook independiente para Colab. No se afirma que v2 ya se haya vuelto a ejecutar allí.

La comparación controlada usa las mismas dependencias y solo casos comunes. Estas métricas pertenecen a la evaluación previa al reajuste final, no a resultados observados de 2027.

| Año / casos comunes | Modelo | ROC-AUC | Brier | Average precision |
| --- | --- | ---: | ---: | ---: |
| 2024 / 2,815 | v1 local | 0.681023 | 0.224477 | 0.729499 |
| 2024 / 2,815 | v2 local | 0.681422 | 0.224488 | 0.729493 |
| 2025 / 2,772 | v1 local | 0.738589 | 0.207028 | 0.777394 |
| 2025 / 2,772 | v2 local | 0.738773 | 0.206989 | 0.777256 |

El desempeño se mantiene prácticamente igual; el beneficio de v2 es restringir la emisión geográficamente. Mayor ROC-AUC/AP y menor Brier son mejores; AUC no es porcentaje de aciertos y AP no es PR-AUC trapezoidal. Los años ya se habían observado durante v1 y la auditoría: esta comparación no constituye una nueva prueba independiente. No hay calibración adicional ni explicaciones individuales calculadas. La instantánea revisada de 2026 tampoco reproduce la disponibilidad histórica exacta de publicaciones.

## 5. Arquitectura e integración verificadas

El flujo implementado es: datasets originales, notebook Python, preparación y entrenamiento, exportación CSV/JSON y modelo, importación validada en SQLite, API FastAPI y dashboard React con TypeScript/Vite. Leaflet presenta los límites oficiales Census. El modelo calcula resultados fuera de la consulta; la API sirve predicciones precalculadas. La API no deserializa el archivo joblib.

La activación selecciona una única versión por año objetivo. Antes de activarla se compara el conjunto de probabilidades de SQLite con el CSV, se valida su política y se crea un respaldo. Una selección sin resultado devuelve ausencia explícita, aunque exista una predicción anterior. El historial omite pares en cuarentena sin borrar los registros originales; los 73,327 registros históricos almacenados no equivalen a registros íntegramente validados.

El contrato incluye FIPS de cinco caracteres, año objetivo, probabilidad de 0 a 1, corte, fecha de generación, versión, estado experimental y procedencia demo/real. Historial y tarjeta se consultan con la misma versión. Un cambio de versión durante la consulta se comunica para volver a consultar.

El mapa comienza en Estados Unidos por estados; al pulsar un estado aparecen sus condados. Filtros y selección se sincronizan, con botón para regresar. Gris significa ausencia, no probabilidad cero. Los colores nacionales no agregan probabilidades estatales. Alaska y Hawaii se reubican únicamente en la vista nacional, con aviso de escala distinta.

El repositorio contiene código, notebooks, pruebas y documentación. Los datasets, modelos, bases SQLite, respaldos y configuraciones locales permanecen fuera de Git. El README describe instalación, importación, geografía y activación. Subir el código no publica la aplicación ni incluye automáticamente los artefactos de datos.

## 6. EDT y criterios de aceptación

Nivel 1: FloodRisk. Nivel 2: entregables principales. Nivel 3: paquetes verificables. No se añaden niveles vacíos; la imagen docente recomienda no superar seis niveles, sujeto a confirmar la rúbrica.

| Código | Entregable o paquete | Criterio / estado |
| --- | --- | --- |
| 1.1 | Gestión y documentación | Alcance y seguimiento por materia |
| 1.1.1 | Requisitos y EDT | Propuesta actualizada; rúbricas pendientes |
| 1.1.2 | Memoria y evidencias | Informe actualizado; aportaciones por confirmar |
| 1.2 | Datos preparados | Política reproducible y excepciones trazables |
| 1.2.1 | Auditoría y geografía | Revisión inicial y 2025 hechas; serie completa pendiente |
| 1.2.2 | Variables y etiqueta | Pipeline v2 implementado |
| 1.3 | Modelo experimental | Evaluación y exportación reproducibles |
| 1.3.1 | Referencia y candidatos | Comparados; logística seleccionada |
| 1.3.2 | Evaluación y exportación | Métricas, política y 2,866 resultados disponibles |
| 1.4 | Prototipo e interfaz | Recorrido coherente y demostrable |
| 1.4.1 | Figma navegable móvil y escritorio | Recorridos conectados; aceptación del equipo pendiente |
| 1.4.2 | Dashboard y mapa | Implementados; comparación final con Figma pendiente |
| 1.5 | Servicio y verificación | Consultas consistentes por versión |
| 1.5.1 | SQLite y API | v2 importada y activa; respaldos conservados |
| 1.5.2 | Pruebas y demostración | 16 pruebas y build correctos; aceptación del equipo pendiente |

Los criterios de software exigen coincidencia CSV/API/mapa, ausencia explícita sin recurrir a v1, historial compatible y navegación usable. La aceptación académica exige además recorrido Figma, evidencia de ejecución y seguimiento, capturas y contribuciones reales. Las pruebas de software no acreditan calidad predictiva ni aprobación docente.

## 7. Plan restante, recursos y riesgos

La reunión de Formulación del 16 de octubre menciona entrega el 6 de noviembre de 2026; confirmar hora, medio y requisitos de las etapas 3 y 4. No se traslada esa fecha a Fundamentos de IA, cuya rúbrica y fecha siguen por confirmar.

| Periodo propuesto | Prioridad y evidencia esperada |
| --- | --- |
| 19 a 23 de octubre | Confirmar rúbricas; adaptar móvil y documentación; reproducir instalación en otro equipo |
| 26 a 30 de octubre | Comparar Figma/web; validar Safari real; revisar IA; recopilar aportaciones |
| 2 a 6 de noviembre | Revisar memoria, enlaces y demostración; preparar entrega de Formulación |

El entrenamiento e integración ya realizados no se vuelven a presupuestar como pendientes. La estimación anterior de 120 horas persona era un supuesto de capacidad, no tiempo consumido ni compromiso confirmado. El equipo debe estimar y asignar el trabajo restante según disponibilidad real. Se prevé usar equipos, conexión, herramientas locales y Colab disponibles; desembolso adicional previsto cero, sin afirmar que el esfuerzo sea gratuito. No se calculan ROI ni beneficios económicos no medidos.

| Riesgo | Tratamiento actual y siguiente acción |
| --- | --- |
| Etiqueta amplia y cobertura condicionada | Mostrar definición experimental; mantener visible la limitación |
| Geografía histórica incompleta | Política v2 y cuarentena; continuar auditoría por años |
| Publicación posterior y prueba reutilizada | Documentar evaluación retrospectiva; nuevo esquema para ajustes futuros |
| Probabilidades no calibradas | Reportar Brier; evaluar calibración sin reutilizar prueba como selección |
| Confusión de versiones | Activación única, validación exacta, respaldo y ausencia explícita |
| Diferencias entre materias | Confirmar rúbricas y separar evidencias y fechas |
| Falta de evidencias individuales | Registrar contribuciones reales, sin atribuciones inventadas |

En cada revisión se registran tarjeta, evidencia, responsable acordado, bloqueos y esfuerzo real. Los cambios de objetivo o nuevas funciones requieren actualizar alcance y capacidad. No se asumen firmas, entregas ni aprobaciones existentes.

## 8. Evidencias, uso y próximos entregables

Al 17 de octubre: 16 pruebas automatizadas correctas y compilación de frontend correcta. Se verificó la exclusión de los 122 códigos, la cuarentena histórica y la coincidencia de 2,866 probabilidades en los mapas de 51 estados/DC. La revisión visual inicial del navegador y móvil corresponde a la integración anterior; no sustituye una nueva aceptación visual de v2 por el equipo.

Para demostrar: iniciar API y web según README; abrir la vista nacional; seleccionar Texas y un condado con resultado; verificar año 2027, corte 2025 y versión experimental-v2-geo; seleccionar un área sin resultado y comprobar el mensaje y el mapa; revisar historial y metodología. La aplicación funciona localmente; los puertos concretos dependen de los procesos disponibles.

Los siguientes entregables son la aceptación del recorrido móvil/escritorio, Safari real, comparación con la interfaz, reproducción por otro integrante y paquete académico con aportaciones individuales. La calibración y las explicaciones siguen como trabajo de IA por priorizar; el despliegue público es posterior y opcional para una demo local. No se declara terminado todo el proyecto.

## 9. Diseño primero en móvil y compatibilidad

La aplicación sigue siendo una sola web React/TypeScript con Vite, Leaflet y API FastAPI. El CSS parte de una columna móvil y amplía la distribución para escritorio. Se ajustan navegación, filtros, controles táctiles, textos largos e historial sin modificar el modelo ni las probabilidades de v2. Los selectores usan 16 px y altura de 48 px; los controles principales, al menos 44 px.

El navegador consulta /api en el mismo origen. El proxy de desarrollo dirige las solicitudes a 127.0.0.1:8000 en el equipo y evita que un teléfono consulte su propio localhost. Un despliegue requiere un proxy equivalente o configurar una URL de API autorizada. La aplicación no se convierte automáticamente en app nativa ni en servicio publicado.

Se combinan jerarquía geográfica, vistas filtradas y tarjetas de resumen. El prototipo móvil conserva doce pantallas y tres filtros superpuestos editables, mapas vectoriales y un punto de inicio propio. Se validaron 89 destinos sin saltos al escritorio y tipografía Inter; no contiene una captura aplanada de la interfaz.

Los resultados actuales de navegador se registran en docs/compatibilidad.md y docs/evidence/mobile/results.json. Debe distinguirse una compilación correcta, pruebas funcionales por motor y validación en dispositivos físicos. WebKit automatizado no acredita Safari real ni todas sus versiones. La revisión manual en iPhone/Mac y la aceptación del docente permanecen pendientes.

El requisito procede de los apuntes y de la aclaración del estudiante sobre la explicación oral del profesor. Las fotos muestran seis modelos de organización y reglas de legibilidad, funcionalidad, consistencia y pruebas; no confirman una rúbrica ni versiones de navegador específicas.

Documentos por materia: docs/fundamentos_ia_actualizado.md y docs/formulacion_actualizada.md. Estas revisiones alinean objetivos y evidencias con la implementación; los originales sincronizados y el informe v3 se conservan como antecedentes.

Prototipo móvil: https://www.figma.com/proto/CDXLWi9tsG9jdzsIWuZ3eV?node-id=57-4178&starting-point-node-id=57%3A4178&scaling=scale-down . Escritorio: mismo archivo, inicio 18:17. Apuntes: https://app.notion.com/p/4019d94868e680a982d2eeb4cf8cd620 .

### Fuentes y trazabilidad

- Código e instrucciones: https://github.com/Kolmersito/floodrisk. Notebooks 02_entrenamiento_floodrisk.ipynb y 03_entrenamiento_floodrisk_v2_geografia.ipynb; tests y README.
- Actividades: https://trello.com/b/hImFh8J2/floodrisk-desarrollo-del-prototipo. Diseño: https://www.figma.com/design/CDXLWi9tsG9jdzsIWuZ3eV?node-id=1-2.
- Material docente: 002_Fundamentos_proyectosTI.pdf, páginas 11 y 12 sobre ejecución y monitoreo; imagen de niveles de EDT. Son referencias conceptuales, no rúbrica confirmada.
- Reunión de Formulación: https://app.notion.com/p/3fb9d94868e6806282ede8f3114731cc. Documentos anteriores de diseño y planificación: antecedentes de alcance e integrantes, no evidencia de resultados actuales.
- Evidencias locales: FloodRisk_auditoria_inicial.zip; metadatos.json, politica_geografica.json y métricas del export floodrisk_modelo_v2.zip; comparacion_misma_poblacion.csv; diagnóstico geográfico. Los originales se conservan.
- Paquete original: Riesgo de inundaciones para seguros en USA (1).zip. SHA-256: 9dfb8a263c03e36cd0e682a347b69d09b906a2ab183231fb618b67a59ad23753.
- Geometría: U.S. Census Bureau, límites cartográficos 2020/2025; procedencia y hashes en data/geographic/README.md y manifiesto local. NOAA 2025 contrastado: StormEvents_details-ftp_v1.0_d2025_c20260819.csv.gz.

Este informe sustituye el estado técnico del informe anterior; no cambia archivos originales, no acredita entrega académica y no redistribuye los datasets. La fuente editable de este documento se conserva con el código.
