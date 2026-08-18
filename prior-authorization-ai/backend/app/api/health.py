from fastapi import APIRouter
from app.db.mongodb import db_config
from app.db.collections import *

router = APIRouter()

@router.get("/health")
async def health_check():
    db_status = "CONNECTED" if db_config.client is not None else "UNAVAILABLE"
    if db_status == "CONNECTED":
        try:
            await db_config.client.admin.command('ping')
        except Exception:
            db_status = "UNAVAILABLE"

    return {
        "status": "healthy",
        "backend": "FastAPI",
        "database": db_status,
        "database_name": db_config.db.name if db_config.db is not None else None,
        "version": "1.0"
    }

@router.get("/health/db-stats")
async def db_stats():
    if db_config.client is None or db_config.db is None:
        return {"error": "DB unavailable"}
    
    db = db_config.db
    
    cms_colls = [
        CMS_ARTICLES, CMS_ICD_COVERED_ARTICLES, CMS_ICD_NONCOVERED_ARTICLES,
        CMS_ARTICLE_HCPCS, CMS_RELATED_DOCUMENTS, CMS_LCD, CMS_RELATED_NCD,
        CMS_NCD, CMS_CONTRACTORS
    ]
    
    synthea_colls = [
        SYNTHEA_PATIENTS, SYNTHEA_CONDITIONS, SYNTHEA_MEDICATIONS, SYNTHEA_PROCEDURES,
        SYNTHEA_DIAGNOSTIC_RESULTS, SYNTHEA_VITAL_SIGNS, SYNTHEA_ENCOUNTERS,
        SYNTHEA_ALLERGIES, SYNTHEA_IMMUNIZATIONS, SYNTHEA_CARE_PLANS,
        SYNTHEA_SOCIAL_HISTORY, SYNTHEA_SURGERIES, SYNTHEA_FUNCTIONAL_STATUS,
        SYNTHEA_CLINICAL_ASSESSMENTS, SYNTHEA_FAMILY_HISTORY, SYNTHEA_REFERRALS,
        SYNTHEA_MEDICAL_EQUIPMENT, SYNTHEA_CLAIMS, SYNTHEA_COVERAGE,
        SYNTHEA_AUTHORIZATION_REQUESTS, SYNTHEA_PROVIDERS
    ]
    
    aligned_colls = [ALIGNED_PRIOR_AUTH_CASES, ALIGNED_CONDITION_ADDITIONS]
    
    async def count_populated(colls):
        c = 0
        for coll in colls:
            if await db[coll].estimated_document_count() > 0:
                c += 1
        return c
    
    cms_count = await count_populated(cms_colls)
    synthea_count = await count_populated(synthea_colls)
    aligned_count = await count_populated(aligned_colls)
    
    return {
        "cms_collections_populated": cms_count,
        "cms_expected": len(cms_colls),
        "synthea_collections_populated": synthea_count,
        "synthea_expected": len(synthea_colls),
        "aligned_collections_populated": aligned_count,
        "aligned_expected": len(aligned_colls)
    }
