import json
from pathlib import Path
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/audit")
async def get_dataset_audit():
    audit_file = Path('reports/dataset_audit.json')
    if not audit_file.exists():
        raise HTTPException(status_code=404, detail="Audit report not found")
    
    with open(audit_file, 'r') as f:
        data = json.load(f)
    
    return data
