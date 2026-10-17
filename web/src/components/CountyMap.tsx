import { useEffect, useRef, useState } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import '../map.css';
import { getMap } from '../services/api';
import type { MapCollection, MapProperties } from '../services/api';
import { NationalMap } from './NationalMap';

export function probabilityColor(p: number | null): string {
  if (p === null) return '#d8e1e8';
  if (p < 0.25) return '#d2eaf8';
  if (p < 0.5) return '#80bfdc';
  if (p < 0.75) return '#318ebd';
  return '#075782';
}

export function CountyMap(props: {
  state: string; year: number; fips: string; onSelect: (fips: string) => void; onStateSelect: (state: string) => void;
}) {
  const [national,setNational] = useState(true);
  const previousState = useRef(props.state);
  useEffect(() => {
    if (previousState.current !== props.state) { setNational(false); previousState.current = props.state; }
  },[props.state]);
  if (national) return <NationalMap selectedState={props.state} onSelect={code => { props.onStateSelect(code); setNational(false); }} />;
  return <CountyDetailMap {...props} onBackToCountry={() => setNational(true)} />;
}

function CountyDetailMap({ state, year, fips, onSelect, onBackToCountry }: {
  state: string; year: number; fips: string; onSelect: (fips: string) => void; onBackToCountry: () => void;
}) {
  const container = useRef<HTMLDivElement>(null);
  const map = useRef<L.Map | null>(null);
  const polygons = useRef<L.GeoJSON | null>(null);
  const select = useRef(onSelect);
  select.current = onSelect;
  const fittedState = useRef('');
  const [data, setData] = useState<MapCollection>();
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  useEffect(() => {
    if (!container.current) return;
    const instance = L.map(container.current, { scrollWheelZoom: false }).setView([38, -97], 4);
    instance.attributionControl.addAttribution('Límites: U.S. Census Bureau · 2025');
    map.current = instance;
    const observer = new ResizeObserver(() => instance.invalidateSize());
    observer.observe(container.current);
    return () => { observer.disconnect(); instance.remove(); map.current = null; polygons.current = null; fittedState.current = ''; };
  }, []);
  useEffect(() => {
    if (!state) return;
    let active = true;
    setLoading(true); setError(''); setData(undefined);
    polygons.current?.clearLayers();
    getMap(state, year).then(result => { if (active) setData(result); })
      .catch(() => { if (active) setError('No se pudo cargar el mapa. Comprueba la API y la preparación geográfica.'); })
      .finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, [state, year]);
  useEffect(() => {
    const instance = map.current;
    if (!instance || !data) return;
    polygons.current?.remove();
    const layer = L.geoJSON(data, {
      // Alaska cruza el antimeridiano. Mantener sus islas en el mismo lado del mapa.
      coordsToLatLng: coordinates => L.latLng(coordinates[1], state === 'AK' && coordinates[0] > 0 ? coordinates[0] - 360 : coordinates[0]),
      style: feature => ({ fillColor: probabilityColor((feature?.properties as MapProperties).probability),
        fillOpacity: 0.88, color: feature?.properties.county_fips === fips ? '#e68100' : '#ffffff',
        weight: feature?.properties.county_fips === fips ? 3 : 0.8 }),
      onEachFeature: (feature, polygon) => {
        const p = feature.properties as MapProperties;
        const text = `${p.name} · FIPS ${p.county_fips} · ${p.probability === null ? 'Sin predicción disponible' : `${(100*p.probability).toFixed(1)} %${p.is_demo ? ' (demo)' : ' experimental'}`}`;
        const tooltip = document.createElement('span');
        tooltip.textContent = text;
        polygon.bindTooltip(tooltip, { sticky: true });
        polygon.on('click', () => select.current(p.county_fips));
        polygon.on('add', () => {
          const element = (polygon as L.Path).getElement();
          if (!element) return;
          element.setAttribute('tabindex','0'); element.setAttribute('role','button');
          element.setAttribute('aria-label',text);
          element.addEventListener('keydown', event => {
            const key = (event as KeyboardEvent).key;
            if (key === 'Enter' || key === ' ') { event.preventDefault(); select.current(p.county_fips); }
          });
          element.addEventListener('focus', () => polygon.openTooltip());
          element.addEventListener('blur', () => polygon.closeTooltip());
        });
      }
    }).addTo(instance);
    polygons.current = layer;
    layer.eachLayer(polygon => {
      if ((polygon as L.Polygon).feature?.properties.county_fips === fips) (polygon as L.Path).bringToFront();
    });
    if (fittedState.current !== state && layer.getBounds().isValid()) {
      instance.fitBounds(layer.getBounds(), { padding:[15,15] }); fittedState.current = state;
    }
  }, [data, fips, state]);
  const zoom = (selected: boolean) => {
    const instance = map.current, layer = polygons.current;
    if (!instance || !layer) return;
    if (selected) layer.eachLayer(polygon => {
      if ((polygon as L.Polygon).feature?.properties.county_fips === fips)
        instance.fitBounds((polygon as L.Polygon).getBounds(), { padding:[30,30], maxZoom:11 });
    });
    else if (layer.getBounds().isValid()) instance.fitBounds(layer.getBounds(), { padding:[15,15] });
  };
  const hasPolygon = data?.features.some(f => f.properties.county_fips === fips);
  return <section className="panel geographic-panel">
    <div className="map-heading"><div><h2>Explora los condados · {state}</h2><p>Selecciona un área para consultar su resultado de {year}.</p></div><div className="map-actions" role="group" aria-label="Navegación del mapa"><button onClick={onBackToCountry}>← Volver al país</button><button onClick={() => zoom(false)} disabled={!data}>Ver estado</button><button onClick={() => zoom(true)} disabled={!hasPolygon}>Acercar selección</button></div></div>
    {loading && <p role="status">Cargando límites y predicciones…</p>}
    {error && <p role="alert">{error}</p>}
    <div ref={container} className="county-map" aria-label={`Mapa interactivo de condados de ${state}`} />
    <div className="map-legend" aria-label="Leyenda de probabilidad experimental">
      {[[null,'Sin predicción'],[0.1,'0–<25 %'],[0.3,'25–<50 %'],[0.6,'50–<75 %'],[0.9,'75–100 %']].map(([p,label]) => <span key={String(label)}><i style={{background:probabilityColor(p as number | null)}} />{label}</span>)}
      <span><i className="selected-swatch" />Selección</span>
    </div>
    {data && <small>Versión activa: {data.metadata.active_version ?? '—'}. {data.metadata.n_with_prediction} de {data.features.length} áreas del mapa tienen resultado. Los colores son intervalos visuales, no categorías oficiales de riesgo.</small>}
    {data && !hasPolygon && <p className="map-warning">El código seleccionado no tiene límites coincidentes en el catálogo de 2025. Su resultado no se asigna a otra área.</p>}
    {!!data?.metadata.prediction_codes_without_geometry.length && <p className="map-warning">{data.metadata.prediction_codes_without_geometry.length} códigos con resultado en este estado no tienen polígono coincidente. Pueden consultarse por código, sin ubicarlos artificialmente.</p>}
    <small className="map-source"><a href="https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.html" target="_blank" rel="noreferrer">U.S. Census Bureau · Límites generalizados 2025, escala 1:5,000,000</a>. Sin mapas base externos. Los equivalentes de condado están incluidos.</small>
  </section>;
}
