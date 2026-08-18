from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional

from app.repositories.cms_repository import CMSRepository
from app.services.cms_relationship_service import CMSRelationshipService
from app.services.policy_resolution_service import PolicyResolutionService

router = APIRouter(prefix="/api/policies", tags=["Policies"])

class PolicyResolveRequest(BaseModel):
    icd10: str
    hcpcs_cpt: str
    state: Optional[str] = ""

def get_policy_resolution_service() -> PolicyResolutionService:
    repo = CMSRepository()
    cms_service = CMSRelationshipService(repo)
    return PolicyResolutionService(cms_service)

@router.post("/resolve")
async def resolve_policy(
    request: PolicyResolveRequest,
    service: PolicyResolutionService = Depends(get_policy_resolution_service)
) -> Dict[str, Any]:
    """
    Resolves CMS policies deterministically based on ICD-10 and HCPCS/CPT codes.
    Returns the complete policy graph (Article -> LCD -> NCD).
    """
    if not request.icd10 or not request.hcpcs_cpt:
        raise HTTPException(status_code=400, detail="Both icd10 and hcpcs_cpt codes are required.")

    try:
        result = await service.resolve_policy(
            icd10_code=request.icd10,
            hcpcs_code=request.hcpcs_cpt,
            state=request.state
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
