import sys
import os
import asyncio
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.mongodb import connect_to_mongo, close_mongo_connection
from app.repositories.case_repository import CaseRepository
from app.repositories.synthea_repository import SyntheaRepository
from app.repositories.cms_repository import CMSRepository
from app.services.synthea_service import SyntheaService
from app.services.cms_relationship_service import CMSRelationshipService
from app.services.policy_resolution_service import PolicyResolutionService
from app.services.prior_auth_case_service import PriorAuthCaseService

async def main():
    await connect_to_mongo()
    
    case_repo = CaseRepository()
    cms_repo = CMSRepository()
    synthea_service = SyntheaService()
    policy_resolution_service = PolicyResolutionService(CMSRelationshipService(cms_repo))
    
    case_service = PriorAuthCaseService(case_repo, synthea_service, policy_resolution_service)
    
    all_cases = await case_repo.get_all_cases()
    results = []
    
    for raw_case in all_cases:
        case_id = raw_case.get("case_id")
        
        case = await case_service.get_case_by_id(case_id)
        if not case:
            results.append({
                "case_id": case_id,
                "patient_id": raw_case.get("patient_id"),
                "patient_found": False,
                "icd10": raw_case.get("normalized_icd10"),
                "cpt_hcpcs": raw_case.get("cpt_hcpcs_code"),
                "policy_resolved": False,
                "warnings": ["Patient not found or case loading failed"]
            })
            continue

        resolution = await case_service.resolve_policy(case_id)
        
        if resolution and resolution.get("status") == "INTERNAL_SYNTHETIC_CODE":
            results.append({
                "case_id": case_id,
                "patient_id": case.patient_id,
                "patient_found": True,
                "icd10": case.diagnosis.normalized_code,
                "cpt_hcpcs": case.requested_service.normalized_code,
                "policy_resolved": False,
                "warnings": ["INTERNAL_SYNTHETIC_CODE"]
            })
            continue

        validation = resolution.get("validation", {}) if resolution else {}
        resolved_article_id = None
        resolved_lcd_id = None
        ncd_result = None

        if resolution and resolution.get("resolved_policies", {}).get("covered"):
            covered = resolution["resolved_policies"]["covered"][0]
            resolved_article_id = covered.get("article", {}).get("article_id")
            
            lcds = covered.get("lcds", [])
            if lcds:
                resolved_lcd_id = lcds[0].get("lcd", {}).get("lcd_id")
                
                # Check NCD
                ncds = lcds[0].get("ncds", [])
                if ncds:
                    ncd_result = ncds[0].get("ncd", {}).get("document_id") if ncds[0].get("ncd") else None
        
        results.append({
            "case_id": case_id,
            "patient_id": case.patient_id,
            "patient_found": True,
            "icd10": case.diagnosis.normalized_code,
            "cpt_hcpcs": case.requested_service.normalized_code,
            "policy_resolved": validation.get("policy_resolved", False),
            "resolved_article": resolved_article_id,
            "expected_article": case.expected_article_id,
            "article_match": validation.get("expected_article_match", False),
            "resolved_lcd": resolved_lcd_id,
            "expected_lcd": case.expected_lcd_id,
            "lcd_match": validation.get("expected_lcd_match", False),
            "ncd_result": ncd_result,
            "warnings": validation.get("warnings", [])
        })

    # Ensure reports directory exists
    os.makedirs('reports', exist_ok=True)

    # Write JSON
    with open('reports/aligned_case_validation.json', 'w') as f:
        json.dump(results, f, indent=2)

    # Write Markdown
    with open('reports/aligned_case_validation.md', 'w') as f:
        f.write("# Aligned Case Validation Report\n\n")
        f.write("| Case ID | Patient ID | ICD-10 | HCPCS/CPT | Patient Found | Resolved? | Resolved Art | Expected Art | Art Match | Resolved LCD | Expected LCD | LCD Match | NCD | Warnings |\n")
        f.write("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n")
        for r in results:
            warn = ", ".join(r.get('warnings', []))
            f.write(f"| {r['case_id']} | {r['patient_id']} | {r.get('icd10')} | {r.get('cpt_hcpcs')} | {r['patient_found']} | {r['policy_resolved']} | {r.get('resolved_article')} | {r.get('expected_article')} | {r.get('article_match')} | {r.get('resolved_lcd')} | {r.get('expected_lcd')} | {r.get('lcd_match')} | {r.get('ncd_result')} | {warn} |\n")

    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(main())
