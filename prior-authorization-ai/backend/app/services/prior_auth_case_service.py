from typing import List, Dict, Any, Optional
from app.repositories.case_repository import CaseRepository
from app.services.synthea_service import SyntheaService
from app.services.policy_resolution_service import PolicyResolutionService
from app.models.case import (
    PriorAuthCase,
    PatientSummary,
    CodeInfo,
    ClinicalContextSummary,
    ProvenanceRecord
)

class PriorAuthCaseService:
    def __init__(
        self,
        case_repo: CaseRepository,
        synthea_service: SyntheaService,
        policy_resolution_service: PolicyResolutionService
    ):
        self.case_repo = case_repo
        self.synthea_service = synthea_service
        self.policy_resolution_service = policy_resolution_service

    async def get_all_cases(self) -> List[PriorAuthCase]:
        raw_cases = await self.case_repo.get_all_cases()
        cases = []
        for rc in raw_cases:
            try:
                # We do a lightweight build for the list to avoid heavy DB fetches
                # Just validate patient
                patient = await self.synthea_service.get_patient_details(rc.get("patient_id"))
                if not patient:
                    continue # Or handle as PATIENT_NOT_FOUND

                p_summary = PatientSummary(
                    name=f"{patient.get('first_name', '')} {patient.get('last_name', '')}".strip(),
                    age=int(patient.get('age', 0)) if patient.get('age') else None,
                    sex=patient.get('gender')
                )

                diag = CodeInfo(
                    original_code=rc.get("icd10_code", ""),
                    normalized_code=rc.get("normalized_icd10", ""),
                    description=rc.get("icd10_description", ""),
                    source="Policy Aligned Case",
                    source_collection="aligned_prior_auth_cases",
                    source_mongo_id=str(rc.get("_id"))
                )

                req_srv = CodeInfo(
                    original_code=rc.get("cpt_hcpcs_code", ""),
                    normalized_code=rc.get("cpt_hcpcs_code", ""), # Assume HCPCS codes are already normalized if not internal
                    description=rc.get("requested_service", ""),
                    source="Policy Aligned Case",
                    source_collection="aligned_prior_auth_cases",
                    source_mongo_id=str(rc.get("_id"))
                )

                cases.append(PriorAuthCase(
                    case_id=rc.get("case_id"),
                    patient_id=rc.get("patient_id"),
                    patient=p_summary,
                    diagnosis=diag,
                    requested_service=req_srv,
                    clinical_context_summary=ClinicalContextSummary(),
                    expected_article_id=rc.get("cms_article_id"),
                    expected_lcd_id=rc.get("lcd_id")
                ))
            except Exception as e:
                print(f"Error loading case {rc.get('case_id')}: {e}")
                pass
        return cases

    async def get_case_by_id(self, case_id: str) -> Optional[PriorAuthCase]:
        rc = await self.case_repo.get_case_by_id(case_id)
        if not rc:
            return None

        patient_id = rc.get("patient_id")
        patient = await self.synthea_service.get_patient_details(patient_id)
        if not patient:
            return None

        p_summary = PatientSummary(
            name=f"{patient.get('first_name', '')} {patient.get('last_name', '')}".strip(),
            age=int(patient.get('age', 0)) if patient.get('age') else None,
            sex=patient.get('gender')
        )

        # Check if there is an aligned condition addition
        cond_add = await self.case_repo.get_condition_addition_by_case_id(case_id)
        prov = [ProvenanceRecord(
            source_type="POLICY_ALIGNED_SYNTHETIC_DEMO_DATA",
            source_collection="aligned_prior_auth_cases",
            mongo_id=str(rc.get("_id"))
        )]
        
        if cond_add:
            prov.append(ProvenanceRecord(
                source_type="POLICY_ALIGNED_SYNTHETIC_DEMO_DATA",
                source_collection="aligned_condition_additions",
                mongo_id=str(cond_add.get("_id"))
            ))

        diag = CodeInfo(
            original_code=rc.get("icd10_code", ""),
            normalized_code=rc.get("normalized_icd10", ""),
            description=rc.get("icd10_description", ""),
            source="Policy Aligned Case",
            source_collection="aligned_prior_auth_cases",
            source_mongo_id=str(rc.get("_id"))
        )

        req_srv = CodeInfo(
            original_code=rc.get("cpt_hcpcs_code", ""),
            normalized_code=rc.get("cpt_hcpcs_code", ""),
            description=rc.get("requested_service", ""),
            source="Policy Aligned Case",
            source_collection="aligned_prior_auth_cases",
            source_mongo_id=str(rc.get("_id"))
        )

        # Fetch clinical context
        context = await self.synthea_service.get_clinical_context(patient_id)
        cc_summary = ClinicalContextSummary(
            conditions_count=len(context.get("conditions", [])),
            procedures_count=len(context.get("procedures", [])),
            medications_count=len(context.get("medications", [])),
            diagnostics_count=len(context.get("diagnostic_results", [])),
            functional_status_count=len(context.get("functional_status", [])),
            clinical_assessments_count=len(context.get("clinical_assessments", []))
        )

        return PriorAuthCase(
            case_id=rc.get("case_id"),
            patient_id=patient_id,
            patient=p_summary,
            diagnosis=diag,
            requested_service=req_srv,
            clinical_context_summary=cc_summary,
            provenance=prov,
            expected_article_id=rc.get("cms_article_id"),
            expected_lcd_id=rc.get("lcd_id")
        )

    async def resolve_policy(self, case_id: str) -> Optional[Dict[str, Any]]:
        case = await self.get_case_by_id(case_id)
        if not case:
            return None

        # Check for INTERNAL_SYNTHETIC_CODE
        if "DIAG" in case.diagnosis.original_code or "PROC" in case.requested_service.original_code:
            return {"status": "INTERNAL_SYNTHETIC_CODE"}

        # Perform resolution
        resolution = await self.policy_resolution_service.resolve_policy(
            icd10_code=case.diagnosis.normalized_code,
            hcpcs_code=case.requested_service.normalized_code
        )
        
        # Validation
        resolved_covered = resolution.get("resolved_policies", {}).get("covered", [])
        is_resolved = len(resolved_covered) > 0
        
        validation = {
            "patient_valid": True,
            "icd10_valid": True,
            "hcpcs_valid": True,
            "policy_resolved": is_resolved,
            "expected_article_match": False,
            "expected_lcd_match": False,
            "warnings": resolution.get("warnings", [])
        }

        if is_resolved:
            res_art = resolved_covered[0].get("article", {})
            res_art_id = res_art.get("article_id")
            if str(res_art_id) == str(case.expected_article_id):
                validation["expected_article_match"] = True
            
            lcds = resolved_covered[0].get("lcds", [])
            if lcds:
                res_lcd_id = lcds[0].get("lcd", {}).get("lcd_id")
                if str(res_lcd_id) == str(case.expected_lcd_id):
                    validation["expected_lcd_match"] = True

        resolution["validation"] = validation
        return resolution
