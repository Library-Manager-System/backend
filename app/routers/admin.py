from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from auth.jwt_handler import signJWT

router = APIRouter(
    prefix="/admin"
)


@router.get("/", tags=["admin"])
async def read_admin():
    return {
        "username": "admin"
    }


# Login
class Login(BaseModel):
    username: str
    password: str

@router.post("/login", tags=["admin"])
async def login_admin(login: Login):
    # TODO - Check if admin exists in database
    if login.username == "test" and login.password == "test":
        return signJWT(login.username)
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")
