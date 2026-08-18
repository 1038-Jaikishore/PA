import { useEffect, useState } from 'react';

type DatasetItem = { filename: string; status: string; };
type AuditData = { cms: DatasetItem[]; synthea: DatasetItem[]; aligned_cases: DatasetItem[]; };

export const Dashboard = () => {
  const [data, setData] = useState<AuditData | null>(null);
  const [backendStatus, setBackendStatus] = useState<string>('Checking...');

  useEffect(() => {
    fetch('http://localhost:8000/api/health')
      .then(res => {
        if (res.ok) setBackendStatus('Connected');
        else setBackendStatus('Error');
      })
      .catch(() => setBackendStatus('Disconnected'));

    fetch('http://localhost:8000/api/datasets/audit')
      .then(res => res.ok ? res.json() : null)
      .then(setData)
      .catch(console.error);
  }, []);

  const cmsCount = data?.cms.filter(d => d.status === 'Detected').length || 0;
  const syntheaCount = data?.synthea.filter(d => d.status === 'Detected').length || 0;
  const alignedCount = data?.aligned_cases.filter(d => d.status === 'Detected').length || 0;

  const datasetStatus = data ? 'Complete' : 'Checking...';

  return (
    <div className="glass-panel" style={{ padding: '32px' }}>
      <h1>Dashboard</h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginTop: '20px' }}>
        <div className="glass-panel">
          <h2>System Status</h2>
          <ul style={{ listStyleType: 'none', padding: 0, lineHeight: '2' }}>
            <li><strong>Backend:</strong> <span style={{ color: backendStatus === 'Connected' ? '#10b981' : '#ef4444' }}>● {backendStatus}</span></li>
            <li><strong>Dataset Audit:</strong> <span style={{ color: data ? '#10b981' : '#fbbf24' }}>● {datasetStatus}</span></li>
            <li><strong>MongoDB Import:</strong> <span style={{ color: '#9ca3af' }}>○ Not Started</span></li>
            <li><strong>Patient Graph:</strong> <span style={{ color: '#9ca3af' }}>○ Not Started</span></li>
            <li><strong>CMS Policy Engine:</strong> <span style={{ color: '#9ca3af' }}>○ Not Started</span></li>
            <li><strong>Policy RAG:</strong> <span style={{ color: '#9ca3af' }}>○ Not Started</span></li>
            <li><strong>Evidence Engine:</strong> <span style={{ color: '#9ca3af' }}>○ Not Started</span></li>
            <li><strong>Triage Engine:</strong> <span style={{ color: '#9ca3af' }}>○ Not Started</span></li>
            <li><strong>PDF Evaluation:</strong> <span style={{ color: '#9ca3af' }}>○ Not Started</span></li>
          </ul>
        </div>
        
        <div className="glass-panel">
          <h2>Data Progress (Volume 1)</h2>
          <ul style={{ listStyleType: 'none', padding: 0, lineHeight: '2' }}>
            <li><strong>CMS Data:</strong> {cmsCount > 0 ? <span style={{ color: '#10b981' }}>● {cmsCount} / 9 detected</span> : <span>○ 0 / 9 detected</span>}</li>
            <li><strong>Synthea Data:</strong> {syntheaCount > 0 ? <span style={{ color: '#10b981' }}>● {syntheaCount} / 21 detected</span> : <span>○ 0 / 21 detected</span>}</li>
            <li><strong>Aligned Demo Data:</strong> {alignedCount > 0 ? <span style={{ color: '#10b981' }}>● {alignedCount} / 2 detected</span> : <span>○ 0 / 2 detected</span>}</li>
          </ul>
        </div>
      </div>
    </div>
  );
};
