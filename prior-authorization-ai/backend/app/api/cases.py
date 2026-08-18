from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any

from app.repositories.case_repository import CaseRepository
from app.repositories.synthea_repository import SyntheaRepository
from app.repositories.cms_repository import CMSRepository
from app.services.synthea_service import SyntheaService
from app.services.cms_relationship_service import CMSRelationshipService
from app.services.policy_resolution_service import PolicyResolutionService
from app.services.prior_auth_case_service import PriorAuthCaseService
from app.models.case import PriorAuthCase

router = APIRouter(prefix="/api/prior-auth/cases", tags=["Prior Authorization Cases"])

def get_case_service() -> PriorAuthCaseService:
    case_repo = CaseRepository()
    synthea_service = SyntheaService()
    policy_resolution_service = PolicyResolutionService(CMSRelationshipService(CMSRepository()))
    return PriorAuthCaseService(case_repo, synthea_service, policy_resolution_service)

@router.get("", response_model=List[PriorAuthCase])
async def list_cases(service: PriorAuthCaseService = Depends(get_case_service)):
    """
    Returns available aligned demo cases.
    """
    return await service.get_all_cases()

@router.get("/{case_id}", response_model=PriorAuthCase)
async def get_case(case_id: str, service: PriorAuthCaseService = Depends(get_case_service)):
    """
    Returns case details including patient, diagnosis, requested service, context summary, and provenance.
    """
    case = await service.get_case_by_id(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case

@router.post("/{case_id}/resolve-policy")
async def resolve_policy_for_case(case_id: str, service: PriorAuthCaseService = Depends(get_case_service)):
    """
    Runs Volume 3 resolver using real ICD/CPT attached to the aligned case.
    """
    resolution = await service.resolve_policy(case_id)
    if resolution is None:
        raise HTTPException(status_code=404, detail="Case not found")
    
    if resolution.get("status") == "INTERNAL_SYNTHETIC_CODE":
        return {
            "status": "INTERNAL_SYNTHETIC_CODE",
            "message": "This case contains internal synthetic codes that cannot be resolved via CMS."
        }
        
    return resolution
