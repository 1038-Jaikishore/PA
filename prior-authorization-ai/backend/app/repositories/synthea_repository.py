from typing import Dict, Any, List
from app.db.mongodb import get_db
from app.db.collections import *
from bson import ObjectId

def serialize_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
    if not doc:
        return doc
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

class SyntheaRepository:
    def __init__(self):
        self.db = get_db()

    async def get_patients(self, skip: int = 0, limit: int = 50) -> List[Dict[str, Any]]:
        cursor = self.db[SYNTHEA_PATIENTS].find().skip(skip).limit(limit)
        return [serialize_doc(doc) async for doc in cursor]
        
    async def get_patient_count(self) -> int:
        return await self.db[SYNTHEA_PATIENTS].count_documents({})

    async def get_patient_by_id(self, patient_id: str) -> Dict[str, Any]:
        doc = await self.db[SYNTHEA_PATIENTS].find_one({"patient_id": patient_id})
        return serialize_doc(doc) if doc else None

    async def get_related_records(self, collection_name: str, patient_id: str) -> List[Dict[str, Any]]:
        cursor = self.db[collection_name].find({"patient_id": patient_id})
        return [serialize_doc(doc) async for doc in cursor]

    async def get_provider_by_id(self, provider_id: str) -> Dict[str, Any]:
        doc = await self.db[SYNTHEA_PROVIDERS].find_one({"provider_id": provider_id})
        return serialize_doc(doc) if doc else None
