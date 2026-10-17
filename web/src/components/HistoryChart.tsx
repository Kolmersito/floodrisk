import type { HistoryEntry } from '../types';
export function HistoryChart({ entries }: { entries: HistoryEntry[] }) {
  if (!entries.length) return <p>No hay historial disponible.</p>;
  const max = Math.max(1, ...entries.map(e => e.event_count));
  return <div className="chart" role="list" aria-label="Eventos reportados por año">
    {entries.map(entry => <div className="bar-column" role="listitem" key={entry.year} aria-label={`${entry.year}: ${entry.event_count} eventos`}>
      <span>{entry.event_count}</span><div className="bar-track"><div className="bar" style={{ height: `${entry.event_count / max * 100}%` }} /></div><small>{entry.year}</small>
    </div>)}
  </div>;
}
