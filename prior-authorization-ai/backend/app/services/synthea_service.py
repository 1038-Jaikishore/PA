from typing import Dict, Any, List
from app.repositories.synthea_repository import SyntheaRepository
from app.db.collections import *

class SyntheaService:
    def __init__(self):
        self.repo = SyntheaRepository()

    async def get_patients(self, skip: int = 0, limit: int = 50) -> Dict[str, Any]:
        patients = await self.repo.get_patients(skip, limit)
        total = await self.repo.get_patient_count()
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "patients": patients
        }

    async def get_patient_details(self, patient_id: str) -> Dict[str, Any]:
        return await self.repo.get_patient_by_id(patient_id)

    async def get_clinical_context(self, patient_id: str) -> Dict[str, Any]:
        patient = await self.repo.get_patient_by_id(patient_id)
        if not patient:
            return None

        # Fetch related records concurrently or sequentially. We will do sequentially for simplicity, or gather.
        import asyncio
        collections_to_fetch = [
            SYNTHEA_CONDITIONS, SYNTHEA_PROCEDURES, SYNTHEA_MEDICATIONS,
            SYNTHEA_DIAGNOSTIC_RESULTS, SYNTHEA_VITAL_SIGNS, SYNTHEA_ENCOUNTERS,
            SYNTHEA_ALLERGIES, SYNTHEA_IMMUNIZATIONS, SYNTHEA_CARE_PLANS,
            SYNTHEA_SOCIAL_HISTORY, SYNTHEA_SURGERIES, SYNTHEA_FUNCTIONAL_STATUS,
            SYNTHEA_CLINICAL_ASSESSMENTS, SYNTHEA_FAMILY_HISTORY, SYNTHEA_REFERRALS,
            SYNTHEA_MEDICAL_EQUIPMENT, SYNTHEA_CLAIMS, SYNTHEA_COVERAGE
        ]

        tasks = [self.repo.get_related_records(c, patient_id) for c in collections_to_fetch]
        results = await asyncio.gather(*tasks)

        context = {
            "patient": patient,
            "conditions": results[0],
            "procedures": results[1],
            "medications": results[2],
            "diagnostic_results": results[3],
            "vital_signs": results[4],
            "encounters": results[5],
            "allergies": results[6],
            "immunizations": results[7],
            "care_plans": results[8],
            "social_history": results[9],
            "surgeries": results[10],
            "functional_status": results[11],
            "clinical_assessments": results[12],
            "family_history": results[13],
            "referrals": results[14],
            "medical_equipment": results[15],
            "claims": results[16],
            "coverage": results[17],
            "providers": []
        }

        # Resolve providers from encounters
        provider_ids = set()
        for enc in context["encounters"]:
            pid = enc.get("provider_id")
            if pid:
                provider_ids.add(pid)
        
        providers = []
        for pid in provider_ids:
            p = await self.repo.get_provider_by_id(pid)
            if p:
                providers.append(p)
        
        context["providers"] = providers

        return context
