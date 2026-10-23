"""Prepare the new version without overwriting the historical v3 report."""
from pathlib import Path

root = Path(__file__).resolve().parent
text = (root / 'informe_v3.md').read_text(encoding='utf-8')
text = text.replace('Informe versión 3, actualizado el 17 de octubre de 2026.',
                    'Informe versión 4, actualizado el 22 de octubre de 2026.')
text = text.replace('El diseño Figma sigue siendo una base estática. Convertirlo en prototipo navegable, contrastarlo con la web y completar evidencias académicas son los siguientes entregables.',
                    'Figma dispone de un recorrido de escritorio y otro móvil de 390 x 844 px en el mismo archivo, con cinco casos TX/FL, filtros, metodología y acercamientos. La comparación visual sistemática y la aceptación académica requieren evidencia adicional.')
text = text.replace('| 1.4.1 | Figma navegable | Pendiente conectar interacciones |',
                    '| 1.4.1 | Figma navegable móvil y escritorio | Recorridos conectados; aceptación del equipo pendiente |')
text = text.replace('Confirmar rúbricas; conectar Figma; reproducir instalación en otro equipo',
                    'Confirmar rúbricas; adaptar móvil y documentación; reproducir instalación en otro equipo')
text = text.replace('Comparar Figma/web; revisar limitaciones de IA; recopilar capturas y aportaciones',
                    'Comparar Figma/web; validar Safari real; revisar IA; recopilar aportaciones')
text = text.replace('Los siguientes entregables son Figma navegable, comparación con la interfaz, reproducción desde una copia limpia y paquete académico con aportaciones individuales.',
                    'Los siguientes entregables son la aceptación del recorrido móvil/escritorio, Safari real, comparación con la interfaz, reproducción por otro integrante y paquete académico con aportaciones individuales.')
section = '''## 9. Diseño primero en móvil y compatibilidad

La aplicación sigue siendo una sola web React/TypeScript con Vite, Leaflet y API FastAPI. El CSS parte de una columna móvil y amplía la distribución para escritorio. Se ajustan navegación, filtros, controles táctiles, textos largos e historial sin modificar el modelo ni las probabilidades de v2. Los selectores usan 16 px y altura de 48 px; los controles principales, al menos 44 px.

El navegador consulta /api en el mismo origen. El proxy de desarrollo dirige las solicitudes a 127.0.0.1:8000 en el equipo y evita que un teléfono consulte su propio localhost. Un despliegue requiere un proxy equivalente o configurar una URL de API autorizada. La aplicación no se convierte automáticamente en app nativa ni en servicio publicado.

Se combinan jerarquía geográfica, vistas filtradas y tarjetas de resumen. El prototipo móvil conserva doce pantallas y tres filtros superpuestos editables, mapas vectoriales y un punto de inicio propio. Se validaron 89 destinos sin saltos al escritorio y tipografía Inter; no contiene una captura aplanada de la interfaz.

Los resultados actuales de navegador se registran en docs/compatibilidad.md y docs/evidence/mobile/results.json. Debe distinguirse una compilación correcta, pruebas funcionales por motor y validación en dispositivos físicos. WebKit automatizado no acredita Safari real ni todas sus versiones. La revisión manual en iPhone/Mac y la aceptación del docente permanecen pendientes.

El requisito procede de los apuntes y de la aclaración del estudiante sobre la explicación oral del profesor. Las fotos muestran seis modelos de organización y reglas de legibilidad, funcionalidad, consistencia y pruebas; no confirman una rúbrica ni versiones de navegador específicas.

Documentos por materia: docs/fundamentos_ia_actualizado.md y docs/formulacion_actualizada.md. Estas revisiones alinean objetivos y evidencias con la implementación; los originales sincronizados y el informe v3 se conservan como antecedentes.

Prototipo móvil: https://www.figma.com/proto/CDXLWi9tsG9jdzsIWuZ3eV?node-id=57-4178&starting-point-node-id=57%3A4178&scaling=scale-down . Escritorio: mismo archivo, inicio 18:17. Apuntes: https://app.notion.com/p/4019d94868e680a982d2eeb4cf8cd620 .

'''
text = text.replace('### Fuentes y trazabilidad', section + '### Fuentes y trazabilidad')
(root / 'informe_v4.md').write_text(text, encoding='utf-8')
