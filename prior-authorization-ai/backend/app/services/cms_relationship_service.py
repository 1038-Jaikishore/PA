import re
from typing import List, Dict, Any, Optional
from app.repositories.cms_repository import CMSRepository

class CMSRelationshipService:
    def __init__(self, repository: CMSRepository):
        self.repo = repository

    def normalize_code(self, code: str, code_type: str = "") -> str:
        """
        Normalizes a code by stripping whitespace and converting to uppercase.
        Removes all periods for ICD-10.
        """
        if not code:
            return ""
        normalized = code.strip().upper()
        if code_type.lower() == "icd10":
            normalized = normalized.replace(".", "")
        return normalized

    async def get_icd_coverage(self, normalized_icd: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Looks up covered and non-covered articles for a given ICD-10 code.
        """
        covered = await self.repo.find_covered_articles_by_icd10(normalized_icd)
        non_covered = await self.repo.find_noncovered_articles_by_icd10(normalized_icd)
        return {
            "covered": covered,
            "non_covered": non_covered
        }

    async def get_hcpcs_articles(self, normalized_hcpcs: str) -> List[Dict[str, Any]]:
        """
        Looks up articles related to a given HCPCS code.
        """
        return await self.repo.find_articles_by_hcpcs(normalized_hcpcs)

    def intersect_articles(self, icd_articles: List[Dict[str, Any]], hcpcs_articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Finds articles that exist in both lists by comparing article_id.
        Since versions might differ, we match purely on article_id.
        """
        icd_ids = {str(a.get("article_id")) for a in icd_articles if a.get("article_id")}
        intersection = []
        # Return the hcpcs_article side of the intersection to keep the format consistent
        for ha in hcpcs_articles:
            if str(ha.get("article_id")) in icd_ids:
                intersection.append(ha)
                
        # Deduplicate intersection just in case
        unique_intersection = []
        seen = set()
        for a in intersection:
            aid = str(a.get("article_id"))
            if aid not in seen:
                seen.add(aid)
                unique_intersection.append(a)
                
        return unique_intersection

    async def build_policy_graph(self, article_id: str, article_version: Optional[str] = None) -> Dict[str, Any]:
        """
        Given a matched article, fetches the Master Article, then resolves the LCD, then resolves the NCD.
        Builds a comprehensive tree to return to the frontend.
        """
        # 1. Fetch Master Article
        master_article = await self.repo.get_article(article_id, article_version)
        if not master_article:
            # If version mismatch or not found, try without version
            master_article = await self.repo.get_article(article_id)
            
        graph = {
            "article": master_article,
            "lcds": []
        }

        # 2. Find Related LCDs
        related_lcd_docs = await self.repo.find_lcds_by_article(article_id)
        
        for r_lcd in related_lcd_docs:
            lcd_id = r_lcd.get("lcd_id")
            lcd_version = r_lcd.get("lcd_version")
            if not lcd_id:
                continue
                
            # Fetch Master LCD
            master_lcd = await self.repo.get_lcd(lcd_id, lcd_version)
            if not master_lcd:
                master_lcd = await self.repo.get_lcd(lcd_id)
                
            lcd_node = {
                "lcd": master_lcd,
                "ncds": []
            }
            
            # 3. Find Related NCDs
            related_ncd_docs = await self.repo.find_ncds_by_lcd(lcd_id)
            for r_ncd in related_ncd_docs:
                ncd_id = str(r_ncd.get("r_ncd_id", "")).strip()
                # Invalid or placeholder NCDs like '0' should be skipped or flagged
                if not ncd_id or ncd_id == "0":
                    lcd_node["ncds"].append({
                        "ncd": None,
                        "status": "NO_RELATED_NCD",
                        "raw_relation": r_ncd
                    })
                    continue
                    
                ncd_version = r_ncd.get("r_ncd_version")
                # Fetch Master NCD
                master_ncd = await self.repo.get_ncd(ncd_id, ncd_version)
                if not master_ncd:
                    master_ncd = await self.repo.get_ncd(ncd_id)
                    
                lcd_node["ncds"].append({
                    "ncd": master_ncd,
                    "status": "RESOLVED" if master_ncd else "NOT_FOUND",
                    "raw_relation": r_ncd
                })
                
            graph["lcds"].append(lcd_node)
            
        return graph
