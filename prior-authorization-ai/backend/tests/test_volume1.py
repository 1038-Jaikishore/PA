import pytest
from app.services.code_normalizer import normalize_icd10, normalize_cpt_hcpcs

def test_normalize_icd10():
    assert normalize_icd10("m17.11") == "M17.11"
    assert normalize_icd10(" M17.11 ") == "M17.11"
    assert normalize_icd10(None) is None

def test_normalize_cpt_hcpcs():
    assert normalize_cpt_hcpcs("CPT27447") == "27447"
    assert normalize_cpt_hcpcs("CPT 27447") == "27447"
    assert normalize_cpt_hcpcs("HCPCS:J7325") == "J7325"
    assert normalize_cpt_hcpcs(" j7325 ") == "J7325"
