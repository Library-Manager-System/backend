from fastapi import APIRouter


router = APIRouter(
    prefix="/user"
)


@router.get("/", tags=["user"])
async def read_user():
    return {
        "username": "test"
    }
