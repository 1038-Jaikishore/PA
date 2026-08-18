import asyncio
import logging
from app.db.mongodb import connect_to_mongo, close_mongo_connection, get_db
from app.db.collections import *

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def create_indexes():
    await connect_to_mongo()
    db = get_db()
    if db is None:
        logging.error("Failed to connect to MongoDB.")
        return

    logging.info("Creating indexes for CMS collections...")
    
    # CMS Indexes
    cms_indexes = {
        CMS_ARTICLES: ["article_id"],
        CMS_ICD_COVERED_ARTICLES: ["article_id", "icd10_code_id"],
        CMS_ICD_NONCOVERED_ARTICLES: ["article_id", "icd10_code_id"],
        CMS_ARTICLE_HCPCS: ["article_id", "hcpc_code_id"],
        CMS_RELATED_DOCUMENTS: ["article_id", "r_article_id", "r_lcd_id", "r_ncd_id"],
        CMS_LCD: ["lcd_id"],
        CMS_RELATED_NCD: ["lcd_id", "r_ncd_id"],
        CMS_NCD: ["ncd_id"],
        CMS_CONTRACTORS: ["contractor_id"]
    }

    for coll_name, fields in cms_indexes.items():
        collection = db[coll_name]
        for field in fields:
            try:
                await collection.create_index(field)
                logging.info(f"Created index on {field} for {coll_name}")
            except Exception as e:
                logging.error(f"Failed to create index {field} on {coll_name}: {e}")

    logging.info("Creating indexes for Synthea collections...")
    
    synthea_patient_indexed = [
        SYNTHEA_CONDITIONS, SYNTHEA_MEDICATIONS, SYNTHEA_PROCEDURES, 
        SYNTHEA_DIAGNOSTIC_RESULTS, SYNTHEA_VITAL_SIGNS, SYNTHEA_ENCOUNTERS,
        SYNTHEA_ALLERGIES, SYNTHEA_IMMUNIZATIONS, SYNTHEA_CARE_PLANS,
        SYNTHEA_SOCIAL_HISTORY, SYNTHEA_SURGERIES, SYNTHEA_FUNCTIONAL_STATUS,
        SYNTHEA_CLINICAL_ASSESSMENTS, SYNTHEA_FAMILY_HISTORY, SYNTHEA_REFERRALS,
        SYNTHEA_MEDICAL_EQUIPMENT, SYNTHEA_CLAIMS, SYNTHEA_COVERAGE,
        SYNTHEA_AUTHORIZATION_REQUESTS
    ]

    for coll_name in synthea_patient_indexed:
        collection = db[coll_name]
        try:
            await collection.create_index("patient_id")
            logging.info(f"Created index on patient_id for {coll_name}")
        except Exception as e:
            logging.error(f"Failed to create index patient_id on {coll_name}: {e}")

    # Specific index
    await db[SYNTHEA_PATIENTS].create_index("patient_id", unique=True)
    await db[SYNTHEA_PROVIDERS].create_index("provider_id", unique=True)
    await db[SYNTHEA_ENCOUNTERS].create_index("encounter_id", unique=True)

    # Aligned cases indexes
    await db[ALIGNED_PRIOR_AUTH_CASES].create_index("patient_id")
    await db[ALIGNED_CONDITION_ADDITIONS].create_index("patient_id")

    logging.info("Index creation complete.")
    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(create_indexes())
