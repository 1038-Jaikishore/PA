import os
import asyncio
import pandas as pd
import math
import logging
from app.db.mongodb import connect_to_mongo, close_mongo_connection, get_db
from app.db.collections import *

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

CMS_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "cms")

FILE_TO_COLLECTION = {
    "Article_cleaned.csv": CMS_ARTICLES,
    "ICD10_Covered_MEJ.csv": CMS_ICD_COVERED_ARTICLES,
    "ICD10_NonCovered_MEJ.csv": CMS_ICD_NONCOVERED_ARTICLES,
    "Article_HCPCS.csv": CMS_ARTICLE_HCPCS,
    "Related_Documents.csv": CMS_RELATED_DOCUMENTS,
    "lcd.csv": CMS_LCD,
    "Related_NCD.csv": CMS_RELATED_NCD,
    "NCD.csv": CMS_NCD,
    "Contractor.csv": CMS_CONTRACTORS
}

def clean_value(val):
    if pd.isna(val):
        return None
    if isinstance(val, float) and math.isnan(val):
        return None
    return val

async def import_cms():
    await connect_to_mongo()
    db = get_db()
    if db is None:
        logging.error("Failed to connect to MongoDB.")
        return

    for filename, collection_name in FILE_TO_COLLECTION.items():
        filepath = os.path.join(CMS_DATA_DIR, filename)
        if not os.path.exists(filepath):
            logging.warning(f"File {filename} not found at {filepath}, skipping.")
            continue

        logging.info(f"Importing {filename} to {collection_name}...")
        df = pd.read_csv(filepath, dtype=str)
        
        records = []
        for _, row in df.iterrows():
            record = {k: clean_value(v) for k, v in row.items()}
            record["_source_file"] = filename
            record["_dataset_group"] = "cms"
            
            # Example Normalizations if needed based on rules
            if "hcpc_code_id" in record and record["hcpc_code_id"]:
                record["normalized_hcpcs"] = record["hcpc_code_id"].strip().upper()
                
            records.append(record)

        # Idempotent load: clear and reload
        collection = db[collection_name]
        await collection.delete_many({"_dataset_group": "cms"})
        
        if records:
            # Batch insert to avoid huge memory spikes, though these aren't terribly huge, but lcd.csv is 34MB
            batch_size = 5000
            for i in range(0, len(records), batch_size):
                batch = records[i:i+batch_size]
                await collection.insert_many(batch)
            logging.info(f"Imported {len(records)} records into {collection_name}.")
        else:
            logging.info(f"No records to import for {collection_name}.")

    await close_mongo_connection()
    logging.info("CMS Import complete.")

if __name__ == "__main__":
    asyncio.run(import_cms())
