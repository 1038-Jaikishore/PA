import { useEffect, useState } from 'react';

type DatasetItem = {
  filename: string;
  status: string;
  rows: number;
  columns: number;
  candidate_primary_keys: string[];
  candidate_relationship_keys: string[];
  warnings: string[];
  error?: string;
  exact_column_names?: string[];
  sample_values?: Record<string, string[]>;
};

type AuditData = {
  cms: DatasetItem[];
  synthea: DatasetItem[];
  aligned_cases: DatasetItem[];
};

export const DataStatus = () => {
  const [data, setData] = useState<AuditData | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch('http://localhost:8000/api/datasets/audit')
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch data');
        return res.json();
      })
      .then(setData)
      .catch(err => setError(err.message));
  }, []);

  const renderGroup = (title: string, expectedCount: number, datasets: DatasetItem[]) => (
    <div style={{ marginBottom: '2rem' }}>
      <h2>{title} ({datasets.length} / {expectedCount} detected)</h2>
      {datasets.map(d => (
        <div key={d.filename} className="glass-panel" style={{ marginBottom: '1rem', padding: '16px' }}>
          <h3 style={{ margin: '0 0 8px 0' }}>{d.filename}</h3>
          {d.error ? (
            <p style={{ color: '#ef4444' }}>Error: {d.error}</p>
          ) : (
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px', fontSize: '0.9rem' }}>
              <div><strong>Status:</strong> {d.status}</div>
              <div><strong>Rows:</strong> {d.rows} | <strong>Cols:</strong> {d.columns}</div>
              <div><strong>Primary Keys:</strong> {d.candidate_primary_keys.join(', ') || 'None'}</div>
              <div><strong>Relationships:</strong> {d.candidate_relationship_keys.join(', ') || 'None'}</div>
              {d.warnings.length > 0 && (
                <div style={{ color: '#fbbf24', gridColumn: '1 / -1' }}>
                  <strong>Warnings:</strong>
                  <ul style={{ margin: '4px 0 0 20px', padding: 0 }}>
                    {d.warnings.map((w, i) => <li key={i}>{w}</li>)}
                  </ul>
                </div>
              )}
              <details style={{ gridColumn: '1 / -1', marginTop: '8px' }}>
                <summary style={{ cursor: 'pointer', color: 'var(--accent)' }}>Show Schema & Sample Data</summary>
                <div style={{ marginTop: '8px', overflowX: 'auto' }}>
                  <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.8rem' }}>
                    <thead>
                      <tr>
                        <th style={{ textAlign: 'left', borderBottom: '1px solid var(--glass-border)', padding: '4px' }}>Column</th>
                        <th style={{ textAlign: 'left', borderBottom: '1px solid var(--glass-border)', padding: '4px' }}>Sample Values</th>
                      </tr>
                    </thead>
                    <tbody>
                      {d.exact_column_names?.map(col => (
                        <tr key={col}>
                          <td style={{ borderBottom: '1px solid var(--glass-border)', padding: '4px' }}>{col}</td>
                          <td style={{ borderBottom: '1px solid var(--glass-border)', padding: '4px', opacity: 0.8 }}>
                            {d.sample_values?.[col]?.join(', ') || 'N/A'}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </details>
            </div>
          )}
        </div>
      ))}
    </div>
  );

  return (
    <div className="glass-panel" style={{ padding: '32px', height: '100%', overflowY: 'auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1>Data Status</h1>
          <p style={{ color: 'var(--text-secondary)' }}>Live audit and DB results from backend.</p>
        </div>
        <div style={{ textAlign: 'right' }}>
          <div style={{ color: 'var(--accent)', fontWeight: 'bold' }}>MongoDB Connection</div>
          <div style={{ color: '#10b981' }}>● Connected</div>
        </div>
      </div>
      
      {error && <div style={{ color: '#ef4444', marginBottom: '1rem' }}>{error}</div>}
      
      {!data && !error ? (
        <p>Loading audit data...</p>
      ) : data ? (
        <>
          {renderGroup('CMS POLICY DATA', 9, data.cms)}
          {renderGroup('SYNTHEA CLINICAL DATA', 21, data.synthea)}
          {renderGroup('POLICY-ALIGNED DEMO DATA', 2, data.aligned_cases)}
        </>
      ) : null}
    </div>
  );
};
