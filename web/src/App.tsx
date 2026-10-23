import { useEffect, useState } from 'react';
import { MetricCard } from './components/MetricCard';
import { HistoryChart } from './components/HistoryChart';
import { CountyMap } from './components/CountyMap';
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
    getCatalog().then(c => { if (active) { setCounties(c.counties); setYears(c.years); setFips(c.counties.find(item => item.county_fips === '48201')?.county_fips || c.counties[0]?.county_fips || ''); setYear(c.years.length ? Math.max(...c.years) : 2027); if (!c.counties.length || !c.years.length) { setError('No hay resultados cargados. Consulta el README para importar el ZIP de Colab.'); setLoading(false); } } })
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
  return <div className="shell"><aside><div className="brand">FloodRisk<small>ANÁLISIS DE INUNDACIONES</small></div><nav aria-label="Navegación principal">{['Resumen general', 'Metodología'].map(item => <button key={item} aria-current={page === item ? 'page' : undefined} className={page === item ? 'active' : ''} onClick={() => setPage(item)}>{item}</button>)}</nav><small className="aside-foot">PROTOTIPO ACADÉMICO<br />Resultados experimentales</small></aside>
    <main><header><div><h1>Estimación de eventos relacionados con inundaciones</h1><p>Consulta la estimación anual y los antecedentes de un condado</p></div><span className="badge">{isDemo ? 'DATOS ILUSTRATIVOS' : prediction ? 'MODELO EXPERIMENTAL' : 'SIN RESULTADO CARGADO'}</span></header>
    {page === 'Metodología' ? <Methodology /> : <>
      <div className="filters"><label>Año objetivo<select aria-label="Año objetivo" value={year} disabled={!years.length} onChange={e => setYear(Number(e.target.value))}>{years.map(y => <option key={y}>{y}</option>)}</select></label><label>Estado<select aria-label="Estado" value={state} disabled={!counties.length} onChange={e => setFips(counties.find(c => c.state_code === e.target.value)!.county_fips)}>{[...new Map(counties.map(c => [c.state_code, c.state])).entries()].map(([code, name]) => <option key={code} value={code}>{name}</option>)}</select></label><label className="county-filter">Condado<select aria-label="Condado" value={fips} disabled={!counties.length} onChange={e => setFips(e.target.value)}>{counties.filter(c => c.state_code === state).map(c => <option key={c.county_fips} value={c.county_fips}>{c.name} · FIPS {c.county_fips}</option>)}</select></label></div>
      {error && <div className="panel error" role="alert">{error}</div>}
      {loading && <p role="status">Cargando resultados…</p>}
      {county && county.name_verified === false && !usesMocks && <div className="panel map-warning" role="status">Este código no coincide con los catálogos de condados de 2020/2025. Su predicción se conserva para revisión, pero no representa una ubicación validada.</div>}
      {state && <CountyMap state={state} year={year} fips={fips} onSelect={setFips} onStateSelect={code => { const match = counties.find(c => c.state_code === code && c.geometry_available); if (match) setFips(match.county_fips); }} />}
      {prediction && county && <>
        {!prediction.is_demo && <section className="panel"><p>Estimación experimental de eventos relacionados con inundaciones · Datos hasta {prediction.data_cutoff.slice(0, 4)}.</p><small>Incluye inundaciones, lluvia fuerte, huracanes y marejadas. Cobertura limitada a registros NOAA disponibles; no es un pronóstico meteorológico. Desfase: {prediction.horizon_years ?? '—'} años.</small></section>}
        {page === 'Resumen general' && <><div className="metrics"><MetricCard label="Probabilidad anual experimental" value={probability} note={prediction.is_demo ? 'Valor ficticio · demostración' : `Modelo ${prediction.model_version}`} /><MetricCard label="Condado seleccionado" value={`${county.name}, ${county.state_code}`} note={`FIPS ${county.county_fips}`} /><MetricCard label="Periodo de la estimación" value={`Ene–dic ${year}`} note="Al menos un evento relacionado reportado" /></div>
        <section className="panel"><h2>Sobre la estimación</h2>{prediction.factors.length ? <><p>{prediction.is_demo ? 'Ejemplos ficticios de factores.' : 'Factores asociados, no causas.'}</p><ol>{prediction.factors.map(factor => <li key={factor}>{factor}</li>)}</ol></> : <p>Este archivo no incluye explicaciones individuales. No se atribuyen factores ni causas a este resultado.</p>}<small>Versión: {prediction.model_version}<br />Generado: {new Date(prediction.generated_at).toLocaleString('es')}<br />{prediction.input_snapshot_at && `Instantánea de fuentes: ${new Date(prediction.input_snapshot_at).toLocaleDateString('es')}`}</small></section></>}
        <section className="panel"><h2>Historial de eventos relacionados · {county.name}</h2><p>{history.some(h => h.is_demo) ? 'Valores ficticios para desarrollar la interfaz.' : 'Conteos NOAA por año. Los años ausentes no equivalen a cero eventos.'}</p><HistoryChart entries={history} /></section>
        <footer>Corte de datos: {prediction.data_cutoff} · Año objetivo: {year} · Versión: {prediction.model_version}{isDemo && ' · Demostración, sin modelo entrenado'}</footer>
      </>}
    </>}
    </main></div>;
}
