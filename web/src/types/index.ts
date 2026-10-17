export interface County { county_fips: string; name: string; state: string; state_code: string }
export interface Prediction {
  county_fips: string; target_year: number; probability: number;
  data_cutoff: string; generated_at: string; model_version: string;
  is_demo: boolean; factors: string[];
}
export interface HistoryEntry { county_fips: string; year: number; event_count: number; is_demo: boolean }
export interface Dataset { counties: County[]; predictions: Prediction[]; history: HistoryEntry[] }
