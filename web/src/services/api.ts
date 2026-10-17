import { demo } from '../mocks';
import type { County, Prediction, HistoryEntry } from '../types';

export const usesMocks = import.meta.env.VITE_DATA_MODE !== 'api';
const base = (import.meta.env.VITE_API_URL || 'http://localhost:8000/api').replace(/\/$/, '');
async function request<T>(path: string): Promise<T> {
  const response = await fetch(`${base}${path}`);
  if (!response.ok) throw new Error(response.status === 404 ? 'No hay resultados para esta selección.' : `Error del servidor (${response.status}).`);
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
  const history = await request<HistoryEntry[]>(`/history/${fips}?through_year=${Number(prediction.data_cutoff.slice(0, 4))}`);
  return { prediction, history };
}
