import { useEffect, useState } from 'react';
import { MetricCard } from './components/MetricCard';
import { HistoryChart } from './components/HistoryChart';
import { Methodology } from './pages/Methodology';
import { getCatalog, getResult, usesMocks } from './services/api';
import type { County, HistoryEntry, Prediction } from './types';

export default function App() {
  const [page, setPage] = useState('Resumen general');
  const [counties, setCounties] = useState<County[]>([]);
  const [years, setYears] = useState<number[]>([]);
  const [fips, setFips] = useState('');
  const [year, setYear] = useState(2027);
  const [prediction, setPrediction] = useState<Prediction>();
  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    let active = true;
    getCatalog().then(c => { if (active) { setCounties(c.counties); setYears(c.years); setFips(c.counties[0]?.county_fips || ''); setYear(c.years[0] || 2027); if (!c.counties.length || !c.years.length) { setError('No hay datos cargados. Consulta el README para importar la demo.'); setLoading(false); } } })
      .catch(() => { if (active) { setError('No se pudo consultar la API. Comprueba que esté iniciada.'); setLoading(false); } });
    return () => { active = false; };
  }, []);
  useEffect(() => {
    if (!fips) return;
    let active = true;
    setLoading(true); setError(''); setPrediction(undefined); setHistory([]);
    getResult(fips, year).then(r => { if (active) { setPrediction(r.prediction); setHistory(r.history); } })
      .catch(e => { if (active) setError(e instanceof Error ? e.message : 'No se pudieron cargar los resultados.'); })
      .finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, [fips, year]);
  const county = counties.find(c => c.county_fips === fips);
  const state = county?.state_code || '';
  const probability = prediction ? new Intl.NumberFormat('es', { style: 'percent', maximumFractionDigits: 0 }).format(prediction.probability) : '—';
  const isDemo = usesMocks || prediction?.is_demo || history.some(h => h.is_demo);
  return <div className="shell"><aside><div className="brand">FloodRisk<small>ANÁLISIS DE INUNDACIONES</small></div><nav aria-label="Navegación principal">{['Resumen general', 'Condados', 'Historial', 'Metodología'].map(item => <button key={item} aria-current={page === item ? 'page' : undefined} className={page === item ? 'active' : ''} onClick={() => setPage(item)}>{item}</button>)}</nav><small className="aside-foot">PROTOTIPO ACADÉMICO<br />Modelo en desarrollo</small></aside>
    <main><header><div><h1>Predicción de inundaciones</h1><p>Consulta la estimación anual y los antecedentes de un condado</p></div><span className="badge">{isDemo ? 'DATOS ILUSTRATIVOS' : 'RESULTADOS DEL MODELO'}</span></header>
    {page === 'Metodología' ? <Methodology /> : <>
      <div className="filters"><label>Año objetivo<select value={year} disabled={!years.length} onChange={e => setYear(Number(e.target.value))}>{years.map(y => <option key={y}>{y}</option>)}</select></label><label>Estado<select value={state} disabled={!counties.length} onChange={e => setFips(counties.find(c => c.state_code === e.target.value)!.county_fips)}>{[...new Map(counties.map(c => [c.state_code, c.state])).entries()].map(([code, name]) => <option key={code} value={code}>{name}</option>)}</select></label><label className="county-filter">Condado<select value={fips} disabled={!counties.length} onChange={e => setFips(e.target.value)}>{counties.filter(c => c.state_code === state).map(c => <option key={c.county_fips} value={c.county_fips}>{c.name} · FIPS {c.county_fips}</option>)}</select></label></div>
      {error && <div className="panel error" role="alert">{error}</div>}
      {loading && <p role="status">Cargando resultados…</p>}
      {prediction && county && <>
        {page === 'Resumen general' && <><div className="metrics"><MetricCard label="Probabilidad anual estimada" value={probability} note={prediction.is_demo ? 'Valor ficticio · modelo aún no entrenado' : `Modelo ${prediction.model_version}`} /><MetricCard label="Condado seleccionado" value={`${county.name}, ${county.state_code}`} note={`FIPS ${county.county_fips}`} /><MetricCard label="Periodo de la estimación" value={`Ene–dic ${year}`} note="Al menos una inundación reportada" /></div>
        <div className="detail-grid"><section className="panel"><h2>Comparación geográfica</h2><p>La integración del mapa de condados está pendiente.</p><div className="map-placeholder"><span>Mapa por condado</span><small>GeoJSON y Leaflet · siguiente etapa</small></div></section><section className="panel"><h2>¿Qué influye en la estimación?</h2><p>{prediction.is_demo ? 'Ejemplos de factores; aún no calculados.' : 'Factores asociados a la estimación.'}</p><ol>{prediction.factors.map(factor => <li key={factor}>{factor}</li>)}</ol><small>Su influencia se comprobará al evaluar el modelo.</small></section></div></>}
        {page === 'Condados' && <section className="panel"><h2>Condados disponibles</h2><p>Selecciona un condado para consultar sus resultados.</p><div className="county-list">{counties.map(c => <button key={c.county_fips} onClick={() => { setFips(c.county_fips); setPage('Resumen general'); }}>{c.name}, {c.state} <span>{c.county_fips}</span></button>)}</div></section>}
        {(page === 'Resumen general' || page === 'Historial') && <section className="panel"><h2>Historial de inundaciones · {county.name}</h2><p>{history.some(h => h.is_demo) ? 'Valores ficticios para desarrollar la interfaz.' : 'Eventos reportados por año.'}</p><HistoryChart entries={history} /></section>}
        <footer>Corte de datos: {prediction.data_cutoff} · Año objetivo: {year} · Versión: {prediction.model_version}{isDemo && ' · Demostración, sin modelo entrenado'}</footer>
      </>}
    </>}
    </main></div>;
}
