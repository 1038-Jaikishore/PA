from typing import List, Dict, Any, Optional
from app.db.mongodb import get_db
from app.db.collections import (
    ALIGNED_PRIOR_AUTH_CASES,
    ALIGNED_CONDITION_ADDITIONS
)

class CaseRepository:
    def __init__(self):
        self.db = get_db()

    async def get_all_cases(self) -> List[Dict[str, Any]]:
        if self.db is None:
            self.db = get_db()
        cursor = self.db[ALIGNED_PRIOR_AUTH_CASES].find({})
        return await cursor.to_list(length=None)

    async def get_case_by_id(self, case_id: str) -> Optional[Dict[str, Any]]:
        if self.db is None:
            self.db = get_db()
        return await self.db[ALIGNED_PRIOR_AUTH_CASES].find_one({"case_id": case_id})

    async def get_cases_by_patient_id(self, patient_id: str) -> List[Dict[str, Any]]:
        if self.db is None:
            self.db = get_db()
        cursor = self.db[ALIGNED_PRIOR_AUTH_CASES].find({"patient_id": patient_id})
        return await cursor.to_list(length=None)

    async def get_condition_additions_by_patient_id(self, patient_id: str) -> List[Dict[str, Any]]:
        if self.db is None:
            self.db = get_db()
        cursor = self.db[ALIGNED_CONDITION_ADDITIONS].find({"patient_id": patient_id})
        return await cursor.to_list(length=None)

    async def get_condition_addition_by_case_id(self, case_id: str) -> Optional[Dict[str, Any]]:
        if self.db is None:
            self.db = get_db()
        return await self.db[ALIGNED_CONDITION_ADDITIONS].find_one({"case_id": case_id})
