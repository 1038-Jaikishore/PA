import os
import asyncio
import pandas as pd
import math
import logging
from app.db.mongodb import connect_to_mongo, close_mongo_connection, get_db
from app.db.collections import *

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

SYNTHEA_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "synthea")
ALIGNED_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "aligned_cases")

SYNTHEA_FILE_MAP = {
    "patients.csv": SYNTHEA_PATIENTS,
    "conditions.csv": SYNTHEA_CONDITIONS,
    "medications.csv": SYNTHEA_MEDICATIONS,
    "procedures.csv": SYNTHEA_PROCEDURES,
    "diagnostic_results.csv": SYNTHEA_DIAGNOSTIC_RESULTS,
    "vital_signs.csv": SYNTHEA_VITAL_SIGNS,
    "encounters.csv": SYNTHEA_ENCOUNTERS,
    "allergies.csv": SYNTHEA_ALLERGIES,
    "immunizations.csv": SYNTHEA_IMMUNIZATIONS,
    "care_plans.csv": SYNTHEA_CARE_PLANS,
    "social_history.csv": SYNTHEA_SOCIAL_HISTORY,
    "surgeries.csv": SYNTHEA_SURGERIES,
    "functional_status.csv": SYNTHEA_FUNCTIONAL_STATUS,
    "clinical_assessments.csv": SYNTHEA_CLINICAL_ASSESSMENTS,
    "family_history.csv": SYNTHEA_FAMILY_HISTORY,
    "referrals.csv": SYNTHEA_REFERRALS,
    "medical_equipment.csv": SYNTHEA_MEDICAL_EQUIPMENT,
    "claims.csv": SYNTHEA_CLAIMS,
    "coverage.csv": SYNTHEA_COVERAGE,
    "authorization_requests.csv": SYNTHEA_AUTHORIZATION_REQUESTS,
    "providers.csv": SYNTHEA_PROVIDERS
}

ALIGNED_FILE_MAP = {
    "synthea_cms_policy_aligned_cases.csv": ALIGNED_PRIOR_AUTH_CASES,
    "synthea_condition_additions_for_policy_demo.csv": ALIGNED_CONDITION_ADDITIONS
}

def clean_value(val):
    if pd.isna(val):
        return None
    if isinstance(val, float) and math.isnan(val):
        return None
    return val

def is_synthetic_code(code: str):
    if not code:
        return False
    code = code.upper()
    return code.startswith("DIAG") or code.startswith("PROC")

async def import_data(db, filename, collection_name, directory, group):
    filepath = os.path.join(directory, filename)
    if not os.path.exists(filepath):
        logging.warning(f"File {filename} not found at {filepath}, skipping.")
        return

    logging.info(f"Importing {filename} to {collection_name}...")
    df = pd.read_csv(filepath, dtype=str)
    
    records = []
    for _, row in df.iterrows():
        record = {k: clean_value(v) for k, v in row.items()}
        record["_source_file"] = filename
        record["_dataset_group"] = group
        
        # internal synthetic code rule: preserve them, do not convert them to real codes.
        # But we can add normalized companions for REAL codes if they exist.
        if "procedure_code" in record and record["procedure_code"]:
            code = record["procedure_code"].strip().upper()
            if not is_synthetic_code(code):
                record["normalized_cpt"] = code.replace("CPT", "").replace("HCPCS", "").replace(":", "").strip()
                
        if "icd10_code" in record and record["icd10_code"]:
            code = record["icd10_code"].strip().upper()
            if not is_synthetic_code(code):
                record["normalized_icd10"] = code

        records.append(record)

    collection = db[collection_name]
    await collection.delete_many({"_dataset_group": group})
    
    if records:
        batch_size = 5000
        for i in range(0, len(records), batch_size):
            batch = records[i:i+batch_size]
            await collection.insert_many(batch)
        logging.info(f"Imported {len(records)} records into {collection_name}.")
    else:
        logging.info(f"No records to import for {collection_name}.")


async def import_synthea():
    await connect_to_mongo()
    db = get_db()
    if db is None:
        logging.error("Failed to connect to MongoDB.")
        return

    for filename, collection_name in SYNTHEA_FILE_MAP.items():
        await import_data(db, filename, collection_name, SYNTHEA_DATA_DIR, "synthea")

    for filename, collection_name in ALIGNED_FILE_MAP.items():
        await import_data(db, filename, collection_name, ALIGNED_DATA_DIR, "aligned")

    await close_mongo_connection()
    logging.info("Synthea & Aligned Import complete.")

if __name__ == "__main__":
    asyncio.run(import_synthea())
