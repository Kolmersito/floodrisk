import { demo } from '../mocks';
import type { County, Prediction, HistoryEntry } from '../types';
import type { FeatureCollection, Geometry } from 'geojson';
import type { StateCollection } from '../components/NationalMap';

export async function getStates(): Promise<StateCollection> {
  return request<StateCollection>('/states');
}

export interface MapProperties {
  county_fips: string; name: string; state_code: string; probability: number | null;
  is_demo: boolean | null; model_version: string | null;
}
export type MapCollection = FeatureCollection<Geometry, MapProperties> & {
  metadata: { n_with_prediction: number; prediction_codes_without_geometry: string[]; geometry_year: number; active_version?: string }
};
export async function getMap(state: string, year: number): Promise<MapCollection> {
  const data = await request<MapCollection>(`/map/${state}?target_year=${year}`);
  if (usesMocks) {
    for (const feature of data.features) {
      const prediction = demo.predictions.find(p => p.county_fips === feature.properties.county_fips && p.target_year === year);
      feature.properties.probability = prediction?.probability ?? null;
      feature.properties.is_demo = prediction?.is_demo ?? null;
    }
    data.metadata.n_with_prediction = data.features.filter(f => f.properties.probability !== null).length;
    data.metadata.prediction_codes_without_geometry = [];
  }
  return data;
}

export const usesMocks = import.meta.env.VITE_DATA_MODE === 'mock';
// Same origin works on a phone too; localhost there would refer to the phone.
const base = (import.meta.env.VITE_API_URL || '/api').replace(/\/$/, '');
async function request<T>(path: string): Promise<T> {
  const response = await fetch(`${base}${path}`);
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(typeof body.detail === 'string' ? body.detail : `Error del servidor (${response.status}).`);
  }
  return response.json();
}
export async function getCatalog(): Promise<{ counties: County[]; years: number[] }> {
  if (usesMocks) return { counties: demo.counties, years: [...new Set(demo.predictions.map(p => p.target_year))] };
  const [counties, years] = await Promise.all([request<County[]>('/counties'), request<number[]>('/years')]);
  return { counties, years };
}
export async function getResult(fips: string, year: number): Promise<{ prediction: Prediction; history: HistoryEntry[] }> {
  if (usesMocks) {
    const prediction = demo.predictions.find(p => p.county_fips === fips && p.target_year === year);
    if (!prediction) throw new Error('No hay resultados para esta selección.');
    return { prediction, history: demo.history.filter(h => h.county_fips === fips && h.year < year) };
  }
  const prediction = await request<Prediction>(`/predictions/${fips}?target_year=${year}`);
  const history = await request<HistoryEntry[]>(`/history/${fips}?through_year=${Number(prediction.data_cutoff.slice(0, 4))}&is_demo=${prediction.is_demo}&target_year=${year}&model_version=${encodeURIComponent(prediction.model_version)}`);
  return { prediction, history };
}
