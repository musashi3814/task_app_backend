from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
def ping() -> dict[str, str]:
    return {"message": "pong"}


@router.get("/health-check/")
async def health_check() -> bool:
    return True
