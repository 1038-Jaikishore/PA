import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';

export const PatientCase = () => {
  const { id } = useParams();
  const [context, setContext] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(`http://localhost:8000/api/patients/${id}/clinical-context`)
      .then(res => {
        if (!res.ok) throw new Error('Patient not found');
        return res.json();
      })
      .then(data => {
        setContext(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, [id]);

  if (loading) return <div style={{ padding: '32px' }}>Loading patient context...</div>;
  if (error || !context) return <div style={{ padding: '32px', color: '#ef4444' }}>{error || 'Error loading context.'}</div>;

  const { patient } = context;

  const Section = ({ title, data }: { title: string, data: any[] }) => {
    if (!data || data.length === 0) return null;
    return (
      <details className="glass-panel" style={{ marginBottom: '1rem', padding: '16px' }}>
        <summary style={{ fontWeight: 'bold', cursor: 'pointer', fontSize: '1.1rem' }}>
          {title} ({data.length})
        </summary>
        <div style={{ marginTop: '16px', fontSize: '0.9rem', overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <tbody>
              {data.map((item, idx) => (
                <tr key={idx} style={{ borderBottom: '1px solid var(--glass-border)' }}>
                  <td style={{ padding: '8px' }}>
                    <pre style={{ margin: 0, whiteSpace: 'pre-wrap', fontFamily: 'inherit' }}>
                      {JSON.stringify(item, null, 2)}
                    </pre>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </details>
    );
  };

  return (
    <div style={{ padding: '32px', height: '100%', overflowY: 'auto' }}>
      <div style={{ marginBottom: '20px' }}>
        <Link to="/synthea" style={{ color: 'var(--accent)', textDecoration: 'none' }}>← Back to Directory</Link>
      </div>

      <div className="glass-panel" style={{ padding: '24px', marginBottom: '24px' }}>
        <h1 style={{ margin: '0 0 8px 0' }}>{patient.FIRST} {patient.LAST}</h1>
        <div style={{ color: 'var(--text-secondary)' }}>
          ID: {patient.patient_id} <br />
          Gender: {patient.GENDER} | DOB: {patient.BIRTHDATE} | Address: {patient.ADDRESS}, {patient.CITY}, {patient.STATE}
        </div>
      </div>

      <h2>Clinical Context</h2>
      
      <Section title="Conditions" data={context.conditions} />
      <Section title="Procedures" data={context.procedures} />
      <Section title="Medications" data={context.medications} />
      <Section title="Diagnostic Results" data={context.diagnostic_results} />
      <Section title="Encounters" data={context.encounters} />
      <Section title="Vital Signs" data={context.vital_signs} />
      <Section title="Functional Status" data={context.functional_status} />
      <Section title="Clinical Assessments" data={context.clinical_assessments} />
      <Section title="Surgeries" data={context.surgeries} />
      <Section title="Care Plans" data={context.care_plans} />
      <Section title="Coverage" data={context.coverage} />
      <Section title="Claims" data={context.claims} />
      <Section title="Providers" data={context.providers} />
    </div>
  );
};
