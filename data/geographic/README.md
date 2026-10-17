# Catálogo y límites geográficos

Generados con `python -m api.scripts.prepare_geography`, tras instalar `api/requirements-geography.txt`.

Fuente: U.S. Census Bureau, Cartographic Boundary Files.
https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.html

- Límites: `cb_2025_us_county_5m.zip`, escala 1:5,000,000; 50 estados y Washington D. C., incluyendo equivalentes de condado.
- Nombres históricos suplementarios: `cb_2020_us_county_5m.zip`. No se usan sus polígonos para trasladar predicciones a unidades nuevas.
- `counties_2025.geojson`: geometrías servidas por `/api/map/{state_code}`.
- `states_2025.geojson`: límites estatales oficiales servidos por `/api/states`, fuente `cb_2025_us_state_5m.zip`. Alaska/Hawaii solo se reubican en la vista nacional del navegador, sin cambiar el archivo original.
- `catalog.json`: nombres, estado y disponibilidad de límites por código.
- `source_manifest.json`: URLs, SHA-256, fecha de descarga y códigos con predicción no coincidentes.

Los archivos generados permanecen locales y están excluidos de Git. No son un mapa de peligro físico ni delimitaciones de zonas inundables. Se usa coincidencia exacta de FIPS; no se remapean códigos dudosos. Un código coincidente tampoco garantiza por sí solo la correcta geocodificación de todos los eventos originales.

En la primera preparación se obtuvieron 3,144 áreas actuales y 3,152 nombres entre ambos catálogos. De los 2,988 códigos con predicción, 74 no tienen polígono actual: 8 con nombre histórico de Connecticut y 66 sin correspondencia en ambos catálogos. No interpretar estos últimos como condados validados. La posible mezcla de códigos de zonas meteorológicas debe investigarse en la fuente original antes del siguiente entrenamiento.
