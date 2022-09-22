from fastapi import APIRouter


router = APIRouter(
    prefix="/admin"
)


@router.get("/", tags=["admin"])
async def read_admin():
    return {
        "username": "admin"
    }
