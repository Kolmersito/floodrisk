# FloodRisk: actualización de formulación del proyecto

Universidad Tecnológica de Cancún. Ingeniería en Tecnologías de la Información e Innovación Digital. Grupo LITIID 72. Materia: Formulación de Proyectos. Fecha: 22 de octubre de 2026.

Equipo: Jade Alejandro Morales Millan; Roberto Pablo Angeles García; Kristopher Eiael Cortez Vargas; José Antonio Navarro Galván. La asignación efectiva de tareas y las contribuciones individuales se confirmarán con el equipo.

## 1. Introducción y control de la actualización

FloodRisk es un prototipo académico compartido por Fundamentos de IA y Formulación de Proyectos. Su producto es una aplicación web adaptable para consultar estimaciones experimentales y antecedentes por condado estadounidense. Se adopta el diseño primero en móvil y se amplía después para escritorio, con pruebas entre navegadores y atención especial a Safari.

Esta revisión actualiza el alcance técnico y la planificación del documento inicial de octubre con base en el informe v3 y el repositorio. Conserva el propósito académico y evita presentar el plan empresarial inicial como ejecución real. Las fotografías de clase son referencias conceptuales; no acreditan por sí solas fechas, formatos ni aprobación del docente.

| Cambio | Justificación | Consecuencia |
| --- | --- | --- |
| Una web adaptable, diseñada desde móvil | Aclaración del estudiante sobre la clase | Ajustar Figma, CSS y aceptación |
| Compatibilidad con navegadores | Reglas UX de las diapositivas | Matriz de pruebas y evidencia |
| Safari como prioridad de validación | Explicación oral reportada | Pruebas WebKit y Safari real pendientes de evidencia |
| Prototipo académico vigente | Código y entrenamiento ya existentes | Sustituir promesas empresariales por resultados y pendientes verificables |

## 2. Fase de inicio

Necesidad: facilitar una consulta coherente de fuentes históricas y resultados experimentales por condado, evitando confundir ausencia con probabilidad cero o presentar antecedentes como pronósticos operativos. Los usuarios previstos son estudiantes, evaluadores y personas que revisan el prototipo académico; no se ha acreditado un grupo real de diez analistas ni un patrocinador empresarial.

Objetivo general: entregar un recorrido demostrable desde la selección geográfica hasta la consulta de una estimación anual, sus antecedentes y sus limitaciones, con la misma información en móvil y escritorio.

Objetivos específicos: conservar datos y resultados trazables; presentar año, corte y versión; disponer de un prototipo navegable en Figma; adaptar filtros, mapa e historial a pantallas pequeñas; y documentar pruebas y contribuciones reales.

Viabilidad: se reutilizan React, TypeScript, Vite, Leaflet, FastAPI, SQLite y el pipeline Python ya disponibles. El modelo se entrena fuera de la consulta y no requiere un servidor de modelos de lenguaje. La viabilidad temporal depende del trabajo pendiente y de la disponibilidad real del equipo, incluida la posibilidad de probar Safari en un equipo Apple.

El acta original y su supuesto presupuesto empresarial se consideran antecedentes. No se afirman firmas, autorización de una organización, validación de beneficios económicos ni aceptación del proyecto por un patrocinador. La autorización académica y rúbricas corresponden a los docentes.

## 3. Requisitos y alcance detallado

| ID | Requisito | Criterio de aceptación |
| --- | --- | --- |
| RF-01 | Seleccionar año, estado y condado | La consulta conserva una selección coherente |
| RF-02 | Explorar país, estado y condado | Regresar al país y acercar selección funcionan |
| RF-03 | Presentar resultado e historial | Se muestran corte, versión y procedencia |
| RF-04 | Comunicar ausencia | Brooks sin predicción no aparece como 0 % |
| RF-05 | Consultar metodología | Navegación accesible en móvil y escritorio |
| RNF-01 | Diseño mobile first | Sin desbordamiento de página a 320, 390, 768 y 1440 px |
| RNF-02 | Controles táctiles y legibilidad | Botones principales de al menos 44 px; selectores de 48 px y texto de 16 px |
| RNF-03 | Compatibilidad | Ejecutar los mismos recorridos en Chromium, Firefox y WebKit; registrar Safari real aparte |
| RNF-04 | Acceso desde teléfono | Una web y una API accesibles; configuración documentada sin localhost del teléfono |
| RNF-05 | Errores y accesibilidad básica | Mensajes visibles, foco de teclado y controles etiquetados |
| RNF-06 | Trazabilidad | Código, documentos y evidencias distinguibles de aprobación docente |

La referencia de compilación de la aplicación existente es Chrome/Edge 107, Firefox 104 y Safari 16 o posteriores. Es un objetivo técnico inicial, no evidencia de que se hayan probado esas versiones mínimas. La matriz registra las versiones realmente ejecutadas y debe ampliarse si el docente exige otras.

Se incluyen consultas precalculadas, mapa Census, historial, cinco casos simulados en Figma y documentación. Se excluyen aplicaciones nativas separadas, uso sin conexión garantizado, autenticación, chatbot, alertas, pérdidas económicas previstas y despliegue público obligatorio. El cambio móvil no modifica el algoritmo ni las predicciones existentes.

## 4. EDT, actividades y secuencia

| Código | Paquete verificable | Evidencia o salida |
| --- | --- | --- |
| 1.1 | Gestión y requisitos | Alcance actualizado y criterios por materia |
| 1.1.1 | Confirmación académica | Fecha, rúbrica y formato confirmados por el docente |
| 1.1.2 | Memoria y aportaciones | Documentos y contribuciones reales |
| 1.2 | Datos y modelo | Pipeline, política geográfica y resultados experimentales |
| 1.2.1 | Calidad histórica | Auditoría inicial disponible; serie completa pendiente |
| 1.2.2 | Evaluación | Métricas retrospectivas; calibración por priorizar |
| 1.3 | Prototipo Figma | Recorridos móviles y de escritorio en un archivo |
| 1.3.1 | Móvil | País, TX/FL, cinco condados, filtros y metodología |
| 1.3.2 | Correspondencia web | Comparación con capturas y resolución identificadas |
| 1.4 | Aplicación adaptable | CSS móvil base, ampliaciones y controles táctiles |
| 1.4.1 | API y conexión | Mismo origen /api; guía de acceso desde teléfono |
| 1.4.2 | Estados de interfaz | Carga, ausencia, error, metodología y orientación |
| 1.5 | Verificación y entrega | Evidencia por navegador y paquete reproducible |
| 1.5.1 | Navegadores automatizados | Chromium, Firefox y WebKit con versiones registradas |
| 1.5.2 | Safari real y equipo | iPhone/Mac, reproducción externa y aceptación pendientes |

Secuencia: requisitos, recorrido móvil, adaptación de escritorio, implementación compartida, pruebas funcionales y de compatibilidad, comparación visual y memoria. El entrenamiento ya realizado no se vuelve a planificar como si estuviera pendiente. La compatibilidad se revisa durante la implementación y no solo al final.

## 5. Duraciones y cronograma restante

La reunión de Formulación del 16 de octubre menciona entrega el 6 de noviembre de 2026; siguen por confirmar hora, medio y rúbrica. Esta fecha no se aplica automáticamente a Fundamentos de IA.

| Periodo propuesto | Trabajo | Condición para cerrar |
| --- | --- | --- |
| 22 a 23 de octubre | Adaptación móvil, Figma y documentos | Revisión de cambios y evidencia inicial |
| 26 a 30 de octubre | Safari real, comparación y reproducción | Defectos registrados y corregidos |
| 2 a 6 de noviembre | Memoria y demostración | Aportaciones, enlaces y aceptación del equipo |

Son ventanas propuestas de organización, no compromisos individuales ni una nueva línea base aprobada. Las duraciones y horas persona deben estimarse después de asignar responsables y disponibilidad reales. No se conserva como ejecución el supuesto anterior de 47 días, 1,156.8 horas o producción empresarial.

## 6. Recursos, costos y adquisiciones

Recursos: equipos del grupo, entorno Python/Node, GitHub, Figma y navegador; acceso a un iPhone o Mac para validación real. Se reutilizan dependencias y herramientas del proyecto. No se requiere adquirir una aplicación móvil, cambiar de backend ni contratar inferencia de un modelo de lenguaje para este alcance.

No hay nuevos desembolsos acreditados en esta revisión. El uso de herramientas disponibles no hace que el esfuerzo del equipo sea gratuito. Presupuesto, licencias adicionales o servicios de pruebas remotas deberán acordarse si llegan a ser necesarios. No se presenta el presupuesto empresarial anterior de USD 116,059 ni su VAN/ROI como costo o beneficio real del prototipo.

## 7. Riesgos y respuestas

| Riesgo | Respuesta | Evidencia de cierre |
| --- | --- | --- |
| Diferencias de Safari | Probar WebKit durante desarrollo y Safari real antes de aceptación | Dispositivo, versión, fecha y resultado |
| No disponer de equipo Apple | Registrar pendiente y acordar acceso o servicio con el equipo | Sesión real acreditada; no sustituir por una captura |
| Pantalla estrecha o giro | Anchos 320/390/768/1440 y orientación horizontal | Sin desbordamiento general ni controles inaccesibles |
| Teléfono apunta a localhost propio | /api del mismo origen con proxy de desarrollo | Consulta desde la red local con URL del equipo |
| Confundir ausencia con cero | Mensaje explícito y geometría gris sin resultado | Caso Brooks verificado |
| Documento desactualizado | Referencias por versión y separación de propuesta/evidencia | Informes y README coherentes |
| Etiqueta amplia y calibración pendiente | Limitaciones visibles en cualquier pantalla | Misma advertencia en móvil y escritorio |
| Datos fuera del repositorio | Guía de traslado y reproducción sin versionar bases | Ejecución por otro integrante |

## 8. Comunicaciones y control de cambios

Cada revisión registra cambio, motivo, archivos o pantallas afectados, prueba ejecutada y pendientes. El equipo confirma responsables y aportaciones; no se heredan automáticamente los roles empresariales del documento inicial como horas realizadas.

Este cambio añade requisitos de presentación y compatibilidad al mismo producto. Cualquier aplicación nativa, autenticación, publicación pública o nuevo objetivo de IA requiere revisar alcance, tiempo y recursos. GitHub conserva el código y la documentación; Figma conserva el prototipo. Las materias comparten implementación, pero mantienen entregables y aprobación propios.

## 9. Calidad, aceptación y demostración

La demostración comienza en país, abre Texas, consulta Harris y Travis, comprueba Brooks sin resultado, cambia a Florida para Miami-Dade y Orange, revisa metodología, historial y regreso al país. Los filtros permiten seleccionar territorios pequeños sin depender solo del mapa.

La evidencia de navegador debe registrar resolución, versión, resultado, fecha y limitaciones. Incluye desplazamiento vertical, historial horizontal contenido, controles táctiles, cambios de orientación, mensajes de error y conservación de la información. La matriz y los resultados se mantienen en docs/compatibilidad.md.

WebKit automatizado no se etiqueta como Safari real aprobado. Las pruebas de interfaz tampoco acreditan calibración ni calidad predictiva. La aceptación final del equipo, la revisión del docente y las contribuciones individuales requieren confirmación independiente.

## 10. Conclusión y referencias

La actualización organiza FloodRisk como una sola aplicación web diseñada desde móvil y adaptada a escritorio. El cambio amplía las evidencias de UX y compatibilidad, sin duplicar el proyecto ni alterar sus resultados de IA. El cierre exige pruebas documentadas y una memoria que describa lo efectivamente construido.

Código: https://github.com/Kolmersito/floodrisk . Estado técnico previo: docs/informe_v3.md; actualización compartida: docs/informe_v4.md; informe específico de IA: docs/fundamentos_ia_actualizado.md.

Figma móvil: https://www.figma.com/proto/CDXLWi9tsG9jdzsIWuZ3eV?node-id=57-4178&starting-point-node-id=57%3A4178&scaling=scale-down . Escritorio: mismo archivo, inicio 18:17.

Apuntes de clase: https://app.notion.com/p/4019d94868e680a982d2eeb4cf8cd620 . Reunión de Formulación: https://app.notion.com/p/3fb9d94868e6806282ede8f3114731cc . Las dos fotografías adjuntas muestran modelos de organización y reglas UX. Mobile first y atención a Safari se incorporan a partir de la aclaración oral del estudiante.

Antecedentes conservados: Parcial_Actividad_Fases_Inicio_Planificacion.docx e Informe_Diseno_FloodRisk.pdf. No se modifican los archivos originales sincronizados. Referencias técnicas: https://v7.vite.dev/guide/build y https://playwright.dev/docs/browsers .
