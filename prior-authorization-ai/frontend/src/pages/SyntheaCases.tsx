import { useEffect, useState } from 'react';

type Patient = {
  patient_id: string;
  FIRST?: string;
  LAST?: string;
  GENDER?: string;
  BIRTHDATE?: string;
};

export const SyntheaCases = () => {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/api/patients?limit=50')
      .then(res => res.json())
      .then(data => {
        setPatients(data.patients || []);
        setTotal(data.total || 0);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="glass-panel" style={{ padding: '32px', height: '100%', overflowY: 'auto' }}>
      <h1>Synthea Patient Directory</h1>
      <p style={{ color: 'var(--text-secondary)' }}>
        Browse {total > 0 ? total : ''} synthetic patients.
      </p>

      {loading ? (
        <p>Loading patients...</p>
      ) : (
        <div style={{ display: 'grid', gap: '1rem', marginTop: '1.5rem' }}>
          {patients.map(p => (
            <div key={p.patient_id} className="glass-panel" style={{ padding: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <h3 style={{ margin: '0 0 4px 0' }}>{p.FIRST} {p.LAST}</h3>
                <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                  ID: {p.patient_id} | Gender: {p.GENDER || 'N/A'} | DOB: {p.BIRTHDATE || 'N/A'}
                </div>
              </div>
              <button 
                className="button-primary"
                onClick={() => window.location.href = `/patient/${p.patient_id}`}
              >
                View Clinical Context
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
