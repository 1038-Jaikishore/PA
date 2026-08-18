def normalize_icd10(code: str) -> str:
    if not code or not isinstance(code, str):
        return code
    return code.strip().upper()

def normalize_cpt_hcpcs(code: str) -> str:
    if not code or not isinstance(code, str):
        return code
    code = code.strip().upper()
    code = code.replace("CPT", "").replace("HCPCS", "").replace(":", "").strip()
    return code
