from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class PatientSummary(BaseModel):
    name: str
    age: Optional[int] = None
    sex: Optional[str] = None

class CodeInfo(BaseModel):
    original_code: str
    normalized_code: str
    description: Optional[str] = None
    source: Optional[str] = None
    source_collection: Optional[str] = None
    source_mongo_id: Optional[str] = None

class ClinicalContextSummary(BaseModel):
    conditions_count: int = 0
    procedures_count: int = 0
    medications_count: int = 0
    diagnostics_count: int = 0
    functional_status_count: int = 0
    clinical_assessments_count: int = 0

class ProvenanceRecord(BaseModel):
    source_type: str
    source_collection: str
    mongo_id: str

class PriorAuthCase(BaseModel):
    case_id: str
    case_type: str = "POLICY_ALIGNED_SYNTHETIC_CASE"
    patient_id: str
    patient: PatientSummary
    diagnosis: CodeInfo
    requested_service: CodeInfo
    clinical_context_summary: ClinicalContextSummary
    policy_resolution: Optional[Dict[str, Any]] = None
    provenance: List[ProvenanceRecord] = []
    
    # Expected matches strictly for validation, do not feed into resolution
    expected_article_id: Optional[str] = None
    expected_lcd_id: Optional[str] = None
    
    # Volume 4 Validation
    validation: Optional[Dict[str, Any]] = None
