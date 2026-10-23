import { useEffect, useRef, useState } from 'react';
import L from 'leaflet';
import type { FeatureCollection, Geometry, Position } from 'geojson';
import { getStates } from '../services/api';

export interface StateProperties { state_code: string; name: string }
export type StateCollection = FeatureCollection<Geometry, StateProperties>;

// Insets cartográficos explícitos: los datos originales no se modifican.
function insetCoordinates(value: unknown, code: string): unknown {
  if (!Array.isArray(value)) return value;
  if (typeof value[0] === 'number') {
    let [lon, lat] = value as Position;
    if (code === 'AK') { if (lon > 0) lon -= 360; return [-125+(lon+190)*0.25, 24+(lat-52)*0.25]; }
    if (code === 'HI') return [-108+(lon+161), 24+(lat-18)];
    return value;
  }
  return value.map(item => insetCoordinates(item,code));
}

export function NationalMap({ selectedState, onSelect }: {selectedState: string; onSelect: (state: string) => void}) {
  const element = useRef<HTMLDivElement>(null);
  const map = useRef<L.Map | null>(null);
  const group = useRef<L.GeoJSON | null>(null);
  const select = useRef(onSelect); select.current = onSelect;
  const [data,setData] = useState<StateCollection>();
  const [error,setError] = useState('');
  useEffect(() => {
    let active = true;
    getStates().then(result => { if (active) setData(result); }).catch(() => { if (active) setError('No se pudieron cargar los límites estatales. Comprueba la API.'); });
    return () => { active = false; };
  }, []);
  useEffect(() => {
    if (!element.current) return;
    const instance = L.map(element.current,{scrollWheelZoom:false, zoomAnimation:false, fadeAnimation:false, markerZoomAnimation:false}).setView([38,-97],3);
    instance.attributionControl.addAttribution('Estados: U.S. Census Bureau · 2025');
    map.current = instance;
    const observer = new ResizeObserver(() => {
      instance.invalidateSize();
      if (group.current?.getBounds().isValid()) instance.fitBounds(group.current.getBounds(),{animate:false,padding:[14,14]});
    });
    observer.observe(element.current);
    return () => { observer.disconnect(); instance.stop(); instance.remove(); map.current = null; group.current = null; };
  }, []);
  useEffect(() => {
    if (!data || !map.current) return;
    group.current?.remove();
    const display = structuredClone(data);
    for (const feature of display.features) {
      if ('coordinates' in feature.geometry)
        feature.geometry.coordinates = insetCoordinates(feature.geometry.coordinates,feature.properties.state_code) as typeof feature.geometry.coordinates;
    }
    const layer = L.geoJSON(display,{
      style: feature => ({fillColor:feature?.properties.state_code === selectedState ? '#3c98bd' : '#9dc9df',
        fillOpacity:0.95,color:'#ffffff',weight:1.3}),
      onEachFeature: (feature,polygon) => {
        const props = feature.properties as StateProperties;
        const text = `${props.name} · ${props.state_code} · Ver condados`;
        const tooltip = document.createElement('span'); tooltip.textContent = text;
        polygon.bindTooltip(tooltip,{sticky:true});
        polygon.on('click',() => select.current(props.state_code));
        polygon.on('add',() => {
          const node = (polygon as L.Path).getElement(); if (!node) return;
          node.setAttribute('role','button'); node.setAttribute('tabindex','0'); node.setAttribute('aria-label',text);
          node.addEventListener('keydown',event => {
            if (['Enter',' '].includes((event as KeyboardEvent).key)) { event.preventDefault(); select.current(props.state_code); }
          });
        });
      }
    }).addTo(map.current);
    group.current = layer;
    map.current.fitBounds(layer.getBounds(),{animate:false,padding:[14,14]});
  },[data,selectedState]);
  return <section className="panel geographic-panel">
    <div className="map-heading"><div><h2>Estados Unidos · Explora por estado</h2><p>Haz clic en un estado para ver sus condados y las predicciones.</p></div><span className="badge">PAÍS → ESTADO → CONDADO</span></div>
    {!data && !error && <p role="status">Cargando estados…</p>}
    {error && <p role="alert">{error}</p>}
    <div ref={element} className="county-map national-map" aria-label="Mapa de Estados Unidos dividido por estados" />
    <div className="map-legend"><span><i style={{background:'#9dc9df'}} />Estado · Haz clic para explorar</span><span><i style={{background:'#3c98bd'}} />Estado seleccionado en los filtros</span></div>
    <small>Alaska y Hawaii aparecen reubicados como recuadros cartográficos, a distinta escala. También se incluye Washington D. C. Puedes usar el filtro de estado para áreas pequeñas.</small>
    <small className="map-source">Límites oficiales: U.S. Census Bureau, 2025. Los colores de esta vista no representan probabilidades estatales.</small>
  </section>;
}
