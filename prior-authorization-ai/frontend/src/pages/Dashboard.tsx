import { useEffect, useState } from 'react';

type DBStats = {
  cms_collections_populated: number;
  cms_expected: number;
  synthea_collections_populated: number;
  synthea_expected: number;
  aligned_collections_populated: number;
  aligned_expected: number;
};

export const Dashboard = () => {
  const [dbStatus, setDbStatus] = useState<string>('Checking...');
  const [dbStats, setDbStats] = useState<DBStats | null>(null);

  useEffect(() => {
    fetch('http://localhost:8000/api/health')
      .then(res => res.json())
      .then(data => {
        setDbStatus(data.database);
      })
      .catch(() => setDbStatus('UNAVAILABLE'));

    fetch('http://localhost:8000/api/health/db-stats')
      .then(res => res.ok ? res.json() : null)
      .then(setDbStats)
      .catch(console.error);
  }, []);

  const getStatusText = (actual: number | undefined, expected: number) => {
    if (actual === undefined) return <span>○ Checking...</span>;
    if (actual === expected) return <span style={{ color: '#10b981' }}>● Complete</span>;
    if (actual > 0) return <span style={{ color: '#fbbf24' }}>● Partial ({actual}/{expected})</span>;
    return <span>○ Not Started</span>;
  };

  return (
    <div className="glass-panel" style={{ padding: '32px' }}>
      <h1>Dashboard</h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginTop: '20px' }}>
        <div className="glass-panel">
          <h2>System Status</h2>
          <ul style={{ listStyleType: 'none', padding: 0, lineHeight: '2' }}>
            <li><strong>Backend:</strong> <span style={{ color: '#10b981' }}>● Connected</span></li>
            <li><strong>Dataset Audit:</strong> <span style={{ color: '#10b981' }}>● Complete</span></li>
            <li><strong>MongoDB:</strong> <span style={{ color: dbStatus === 'CONNECTED' ? '#10b981' : '#ef4444' }}>● {dbStatus}</span></li>
            <li><strong>CMS Import:</strong> {getStatusText(dbStats?.cms_collections_populated, 9)}</li>
            <li><strong>Synthea Import:</strong> {getStatusText(dbStats?.synthea_collections_populated, 21)}</li>
            <li><strong>Aligned Demo Import:</strong> {getStatusText(dbStats?.aligned_collections_populated, 2)}</li>
            <li><strong>Patient Graph:</strong> <span style={{ color: dbStats?.synthea_collections_populated === 21 ? '#10b981' : '#9ca3af' }}>{dbStats?.synthea_collections_populated === 21 ? '● Ready' : '○ Not Started'}</span></li>
            <li><strong>CMS Policy Engine:</strong> <span style={{ color: dbStats?.cms_collections_populated === 9 ? '#10b981' : '#9ca3af' }}>{dbStats?.cms_collections_populated === 9 ? '● Ready' : '○ Not Started'}</span></li>
            <li><strong>Policy RAG:</strong> <span style={{ color: '#9ca3af' }}>○ Not Started</span></li>
            <li><strong>Evidence Matching:</strong> <span style={{ color: '#9ca3af' }}>○ Not Started</span></li>
            <li><strong>Triage:</strong> <span style={{ color: '#9ca3af' }}>○ Not Started</span></li>
            <li><strong>PDF Evaluation:</strong> <span style={{ color: '#9ca3af' }}>○ Not Started</span></li>
          </ul>
        </div>
      </div>
    </div>
  );
};
