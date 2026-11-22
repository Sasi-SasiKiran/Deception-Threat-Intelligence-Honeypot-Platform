from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_status():
    return {
        "status": "healthy",
        "service": "internal-ingest-api"
    }
