import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

type PatientSummary = {
  name: string;
  age: number | null;
  sex: string | null;
};

type CodeInfo = {
  original_code: string;
  normalized_code: string;
  description: string;
};

type PriorAuthCase = {
  case_id: string;
  patient_id: string;
  patient: PatientSummary;
  diagnosis: CodeInfo;
  requested_service: CodeInfo;
  expected_article_id: string;
  expected_lcd_id: string;
};

export const PriorAuthCases = () => {
  const [cases, setCases] = useState<PriorAuthCase[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetch('http://localhost:8000/api/prior-auth/cases')
      .then(res => res.json())
      .then(data => {
        setCases(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="glass-panel" style={{ padding: '32px' }}>
      <h1>Prior Auth Cases</h1>
      <p style={{ color: '#9ca3af', marginBottom: '24px' }}>
        These are synthetic aligned cases that map to real CMS policy rules.
      </p>

      {loading ? (
        <p>Loading cases...</p>
      ) : (
        <div style={{ display: 'grid', gap: '16px' }}>
          {cases.map(c => (
            <div 
              key={c.case_id} 
              className="glass-panel hover-glow" 
              style={{ cursor: 'pointer', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}
              onClick={() => navigate(`/prior-auth-cases/${c.case_id}`)}
            >
              <div>
                <h3 style={{ margin: '0 0 8px 0' }}>{c.case_id}</h3>
                <div style={{ color: '#9ca3af', fontSize: '0.9em' }}>
                  <strong>Patient:</strong> {c.patient.name} ({c.patient.age}y {c.patient.sex}) | 
                  <strong> Dx:</strong> {c.diagnosis.original_code} - {c.diagnosis.description} | 
                  <strong> Svc:</strong> {c.requested_service.original_code} - {c.requested_service.description}
                </div>
              </div>
              <div>
                <span className="badge" style={{ background: 'rgba(59, 130, 246, 0.2)', color: '#60a5fa', padding: '4px 8px', borderRadius: '4px' }}>
                  Aligned Case
                </span>
              </div>
            </div>
          ))}
          {cases.length === 0 && <p>No prior auth cases found.</p>}
        </div>
      )}
    </div>
  );
};
