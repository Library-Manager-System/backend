from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel
from auth.jwt_handler import signJWT, decodeJWT
from auth.jwt_bearer import JWTBearer

router = APIRouter(
    prefix="/user"
)


@router.get("/", dependencies=[Depends(JWTBearer())], tags=["user"])
async def read_user(Authorization: str | None = Header(default=None)):
    token_data = decodeJWT(token=Authorization.split(" ")[1])
    if token_data == None: return {"error": "Invalid token"}

    print(Authorization)

    # TODO use user ids
    user = token_data["user"]
    print(user)

    return {
        "username": user
    }


# Login
class Login(BaseModel):
    username: str
    password: str

@router.post("/login", tags=["user"])
async def login_user(login: Login):
    # TODO - Check if user exists in database
    if login.username == "test" and login.password == "test":
        return signJWT(login.username)
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")
