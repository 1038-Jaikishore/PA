import os
import asyncio
import pandas as pd
import logging
from app.db.mongodb import connect_to_mongo, close_mongo_connection, get_db
from scripts.import_cms import FILE_TO_COLLECTION as CMS_MAP, CMS_DATA_DIR
from scripts.import_synthea import SYNTHEA_FILE_MAP, ALIGNED_FILE_MAP, SYNTHEA_DATA_DIR, ALIGNED_DATA_DIR
from app.db.collections import SYNTHEA_PATIENTS, ALIGNED_PRIOR_AUTH_CASES, ALIGNED_CONDITION_ADDITIONS

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def validate_counts():
    await connect_to_mongo()
    db = get_db()
    if db is None:
        logging.error("Failed to connect to MongoDB.")
        return

    all_maps = [
        (CMS_MAP, CMS_DATA_DIR, "CMS"),
        (SYNTHEA_FILE_MAP, SYNTHEA_DATA_DIR, "Synthea"),
        (ALIGNED_FILE_MAP, ALIGNED_DATA_DIR, "Aligned")
    ]

    for file_map, data_dir, group in all_maps:
        logging.info(f"--- Validating {group} ---")
        for filename, coll_name in file_map.items():
            filepath = os.path.join(data_dir, filename)
            if not os.path.exists(filepath):
                logging.warning(f"MISSING FILE: {filename}")
                continue

            # Check rows in CSV
            df = pd.read_csv(filepath, dtype=str)
            csv_count = len(df)
            
            # Check docs in MongoDB
            db_count = await db[coll_name].count_documents({"_source_file": filename})
            
            if csv_count == db_count:
                logging.info(f"PASS: {coll_name} ({csv_count} records)")
            else:
                logging.error(f"MISMATCH: {coll_name} - CSV: {csv_count}, DB: {db_count}")

    # Validate aligned patients
    logging.info("--- Validating Aligned Cases against Synthea Patients ---")
    aligned_cases_coll = db[ALIGNED_PRIOR_AUTH_CASES]
    patients_coll = db[SYNTHEA_PATIENTS]
    
    async for case in aligned_cases_coll.find():
        patient_id = case.get("patient_id")
        if patient_id:
            exists = await patients_coll.find_one({"patient_id": patient_id})
            if exists:
                logging.info(f"MATCHED: aligned case patient_id {patient_id}")
            else:
                logging.error(f"MISSING_PATIENT: aligned case patient_id {patient_id} not in synthea_patients")

    await close_mongo_connection()
    logging.info("Validation complete.")

if __name__ == "__main__":
    asyncio.run(validate_counts())
