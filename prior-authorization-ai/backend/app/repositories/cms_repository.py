from typing import List, Dict, Any, Optional
from app.db.mongodb import get_db
from app.db.collections import (
    CMS_ARTICLES,
    CMS_ICD_COVERED_ARTICLES,
    CMS_ICD_NONCOVERED_ARTICLES,
    CMS_ARTICLE_HCPCS,
    CMS_RELATED_DOCUMENTS,
    CMS_LCD,
    CMS_RELATED_NCD,
    CMS_NCD,
    CMS_CONTRACTORS
)

class CMSRepository:
    def __init__(self):
        # We fetch the DB lazily or at initialization time since lifespan initializes db_config.db
        self.db = get_db()
        
    async def find_covered_articles_by_icd10(self, normalized_icd: str) -> List[Dict[str, Any]]:
        if self.db is None:
            self.db = get_db()
        cursor = self.db[CMS_ICD_COVERED_ARTICLES].find({"icd10_code_id": normalized_icd})
        return await cursor.to_list(length=None)

    async def find_noncovered_articles_by_icd10(self, normalized_icd: str) -> List[Dict[str, Any]]:
        if self.db is None:
            self.db = get_db()
        cursor = self.db[CMS_ICD_NONCOVERED_ARTICLES].find({"icd10_code_id": normalized_icd})
        return await cursor.to_list(length=None)

    async def find_articles_by_hcpcs(self, normalized_hcpcs: str) -> List[Dict[str, Any]]:
        if self.db is None:
            self.db = get_db()
        cursor = self.db[CMS_ARTICLE_HCPCS].find({"hcpc_code_id": normalized_hcpcs})
        return await cursor.to_list(length=None)

    async def get_article(self, article_id: str, version: Optional[str] = None) -> Optional[Dict[str, Any]]:
        if self.db is None:
            self.db = get_db()
        query = {"article_id": article_id}
        if version:
            query["article_version"] = version
        return await self.db[CMS_ARTICLES].find_one(query)

    async def find_lcds_by_article(self, article_id: str) -> List[Dict[str, Any]]:
        if self.db is None:
            self.db = get_db()
        cursor = self.db[CMS_RELATED_DOCUMENTS].find({"r_article_id": article_id})
        return await cursor.to_list(length=None)

    async def get_lcd(self, lcd_id: str, version: Optional[str] = None) -> Optional[Dict[str, Any]]:
        if self.db is None:
            self.db = get_db()
        query = {"lcd_id": lcd_id}
        if version:
            query["lcd_version"] = version
        return await self.db[CMS_LCD].find_one(query)

    async def find_ncds_by_lcd(self, lcd_id: str) -> List[Dict[str, Any]]:
        if self.db is None:
            self.db = get_db()
        cursor = self.db[CMS_RELATED_NCD].find({"lcd_id": lcd_id})
        return await cursor.to_list(length=None)

    async def get_ncd(self, ncd_id: str, version: Optional[str] = None) -> Optional[Dict[str, Any]]:
        if self.db is None:
            self.db = get_db()
        query = {"document_id": ncd_id} # NCD collection uses document_id
        if version:
            query["document_version"] = version
        return await self.db[CMS_NCD].find_one(query)

    async def get_contractor(self, contractor_id: str) -> Optional[Dict[str, Any]]:
        if self.db is None:
            self.db = get_db()
        return await self.db[CMS_CONTRACTORS].find_one({"contractor_id": contractor_id})
