from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "backend": "FastAPI",
        "database": "not_initialized",
        "version": "1.0"
    }
