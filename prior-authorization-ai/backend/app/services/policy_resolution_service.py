from typing import Dict, Any, List
from app.services.cms_relationship_service import CMSRelationshipService

class PolicyResolutionService:
    def __init__(self, cms_service: CMSRelationshipService):
        self.cms_service = cms_service

    async def resolve_policy(self, icd10_code: str, hcpcs_code: str, state: str = "") -> Dict[str, Any]:
        """
        Orchestrates the policy resolution flow:
        1. Look up ICD-10 coverage
        2. Look up HCPCS coverage
        3. Intersect
        4. Build graph
        """
        norm_icd10 = self.cms_service.normalize_code(icd10_code, "icd10")
        norm_hcpcs = self.cms_service.normalize_code(hcpcs_code, "hcpcs")

        # 1. ICD-10 Coverage
        icd_data = await self.cms_service.get_icd_coverage(norm_icd10)
        covered_articles = icd_data["covered"]
        non_covered_articles = icd_data["non_covered"]

        # 2. HCPCS Articles
        hcpcs_articles = await self.cms_service.get_hcpcs_articles(norm_hcpcs)

        # 3. Intersection
        intersected_covered = self.cms_service.intersect_articles(covered_articles, hcpcs_articles)
        intersected_non_covered = self.cms_service.intersect_articles(non_covered_articles, hcpcs_articles)

        # 4. Build graphs for intersected covered articles
        resolved_covered_graphs = []
        for article in intersected_covered:
            article_id = article.get("article_id")
            article_version = article.get("article_version")
            if article_id:
                graph = await self.cms_service.build_policy_graph(article_id, article_version)
                resolved_covered_graphs.append(graph)

        # Build graphs for intersected non-covered articles
        resolved_non_covered_graphs = []
        for article in intersected_non_covered:
            article_id = article.get("article_id")
            article_version = article.get("article_version")
            if article_id:
                graph = await self.cms_service.build_policy_graph(article_id, article_version)
                resolved_non_covered_graphs.append(graph)

        return {
            "inputs": {
                "icd10": icd10_code,
                "normalized_icd10": norm_icd10,
                "hcpcs": hcpcs_code,
                "normalized_hcpcs": norm_hcpcs,
                "state": state
            },
            "intermediate_results": {
                "icd_covered_count": len(covered_articles),
                "icd_non_covered_count": len(non_covered_articles),
                "hcpcs_article_count": len(hcpcs_articles),
                "intersected_covered_count": len(intersected_covered),
                "intersected_non_covered_count": len(intersected_non_covered)
            },
            "resolved_policies": {
                "covered": resolved_covered_graphs,
                "non_covered": resolved_non_covered_graphs
            },
            "jurisdiction_status": "NOT_AVAILABLE_IN_CURRENT_DATASET"
        }
