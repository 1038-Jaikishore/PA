from fastapi import APIRouter, HTTPException, Query, Depends
from app.services.synthea_service import SyntheaService

router = APIRouter()

def get_service():
    return SyntheaService()

@router.get("")
async def get_patients(skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100), service: SyntheaService = Depends(get_service)):
    return await service.get_patients(skip, limit)

@router.get("/{patient_id}")
async def get_patient(patient_id: str, service: SyntheaService = Depends(get_service)):
    patient = await service.get_patient_details(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.get("/{patient_id}/clinical-context")
async def get_patient_clinical_context(patient_id: str, service: SyntheaService = Depends(get_service)):
    context = await service.get_clinical_context(patient_id)
    if not context:
        raise HTTPException(status_code=404, detail="Patient not found")
    return context
