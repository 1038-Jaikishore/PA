import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

type PriorAuthCase = {
  case_id: string;
  patient_id: string;
  patient: {
    name: string;
    age: number | null;
    sex: string | null;
  };
  diagnosis: any;
  requested_service: any;
  clinical_context_summary: any;
  provenance: any[];
};

export const PriorAuthCaseView = () => {
  const { caseId } = useParams();
  const navigate = useNavigate();
  const [caseData, setCaseData] = useState<PriorAuthCase | null>(null);
  const [resolution, setResolution] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [resolving, setResolving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(`http://localhost:8000/api/prior-auth/cases/${caseId}`)
      .then(res => res.json())
      .then(data => {
        if (data.detail) {
          setError(data.detail);
        } else {
          setCaseData(data);
        }
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setError("Failed to fetch case data.");
        setLoading(false);
      });
  }, [caseId]);

  const handleResolve = () => {
    setResolving(true);
    fetch(`http://localhost:8000/api/prior-auth/cases/${caseId}/resolve-policy`, {
      method: 'POST'
    })
      .then(res => res.json())
      .then(data => {
        setResolution(data);
        setResolving(false);
      })
      .catch(err => {
        console.error(err);
        setResolving(false);
      });
  };

  if (loading) return <div className="glass-panel" style={{ padding: '32px' }}>Loading...</div>;
  if (error || !caseData) return <div className="glass-panel" style={{ padding: '32px', color: '#ef4444' }}>Error: {error}</div>;

  return (
    <div style={{ display: 'grid', gap: '24px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        <button 
          onClick={() => navigate('/prior-auth-cases')}
          style={{ background: 'transparent', border: '1px solid #374151', padding: '8px 16px', color: '#fff', borderRadius: '4px', cursor: 'pointer' }}
        >
          ← Back
        </button>
        <h1 style={{ margin: 0 }}>Case {caseData.case_id}</h1>
      </div>

      <div className="glass-panel" style={{ padding: '24px' }}>
        <h2>Patient Summary</h2>
        <p><strong>Name:</strong> {caseData.patient.name} ({caseData.patient.age}y {caseData.patient.sex})</p>
        <p><strong>Patient ID:</strong> {caseData.patient_id}</p>
        
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginTop: '20px' }}>
          <div style={{ background: 'rgba(0,0,0,0.2)', padding: '16px', borderRadius: '8px' }}>
            <h3 style={{ marginTop: 0, color: '#60a5fa' }}>Diagnosis</h3>
            <p><strong>Code:</strong> {caseData.diagnosis.original_code} ({caseData.diagnosis.normalized_code})</p>
            <p><strong>Description:</strong> {caseData.diagnosis.description}</p>
          </div>
          <div style={{ background: 'rgba(0,0,0,0.2)', padding: '16px', borderRadius: '8px' }}>
            <h3 style={{ marginTop: 0, color: '#34d399' }}>Requested Service</h3>
            <p><strong>Code:</strong> {caseData.requested_service.original_code} ({caseData.requested_service.normalized_code})</p>
            <p><strong>Description:</strong> {caseData.requested_service.description}</p>
          </div>
        </div>
      </div>

      <div className="glass-panel" style={{ padding: '24px' }}>
        <h2>Clinical Context Summary</h2>
        <ul style={{ listStyleType: 'none', padding: 0 }}>
          <li>Conditions: {caseData.clinical_context_summary.conditions_count}</li>
          <li>Procedures: {caseData.clinical_context_summary.procedures_count}</li>
          <li>Medications: {caseData.clinical_context_summary.medications_count}</li>
          <li>Diagnostic Results: {caseData.clinical_context_summary.diagnostics_count}</li>
          <li>Clinical Assessments: {caseData.clinical_context_summary.clinical_assessments_count}</li>
        </ul>
      </div>

      <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h2 style={{ margin: 0 }}>Policy Resolution</h2>
          <button 
            onClick={handleResolve}
            disabled={resolving}
            style={{ 
              background: resolving ? '#374151' : '#3b82f6', 
              color: '#fff', 
              border: 'none', 
              padding: '12px 24px', 
              borderRadius: '8px', 
              cursor: resolving ? 'not-allowed' : 'pointer',
              fontWeight: 'bold'
            }}
          >
            {resolving ? 'Resolving...' : 'Resolve CMS Policy'}
          </button>
        </div>

        {resolution && (
          <div style={{ marginTop: '20px', background: 'rgba(0,0,0,0.2)', padding: '20px', borderRadius: '8px' }}>
            {resolution.status === "INTERNAL_SYNTHETIC_CODE" ? (
              <div style={{ color: '#fbbf24' }}>
                <h3>⚠️ Internal Synthetic Code</h3>
                <p>{resolution.message}</p>
              </div>
            ) : (
              <div>
                <h3 style={{ color: resolution.validation?.policy_resolved ? '#10b981' : '#ef4444' }}>
                  {resolution.validation?.policy_resolved ? '● Policy Resolved' : '○ Not Resolved'}
                </h3>
                
                {resolution.validation && (
                  <ul style={{ color: '#9ca3af' }}>
                    <li>Expected Article Match: {resolution.validation.expected_article_match ? 'Yes' : 'No'}</li>
                    <li>Expected LCD Match: {resolution.validation.expected_lcd_match ? 'Yes' : 'No'}</li>
                  </ul>
                )}

                {resolution.resolved_policies?.covered?.length > 0 && (
                  <div style={{ marginTop: '16px' }}>
                    <h4>Resolved Covered Policies:</h4>
                    {resolution.resolved_policies.covered.map((cov: any, idx: number) => (
                      <div key={idx} style={{ background: 'rgba(255,255,255,0.05)', padding: '12px', borderRadius: '4px', marginBottom: '8px' }}>
                        <div><strong>Article:</strong> {cov.article?.article_id} - {cov.article?.description}</div>
                        {cov.lcds?.map((l: any, lidx: number) => (
                          <div key={lidx} style={{ marginLeft: '16px', marginTop: '8px', borderLeft: '2px solid #3b82f6', paddingLeft: '12px' }}>
                            <div><strong>LCD:</strong> {l.lcd?.lcd_id} - {l.lcd?.lcd_title}</div>
                            {l.ncds?.map((n: any, nidx: number) => (
                              <div key={nidx} style={{ marginLeft: '16px', marginTop: '4px' }}>
                                <strong>NCD:</strong> {n.ncd?.document_id || n.status}
                              </div>
                            ))}
                          </div>
                        ))}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>

    </div>
  );
};
