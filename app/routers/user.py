from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel

from auth.jwt_handler import signJWT
from auth.jwt_bearer import JWTBearer
from database.user import User

router = APIRouter(
    prefix="/user"
)


@router.get("/", tags=["user"])
async def read_user(token_data = Depends(JWTBearer())):

    return {
        "email": token_data["email"]
    }


# Login
class Login(BaseModel):
    email: str
    password: str

@router.post("/login", tags=["user"])
async def login_user(login: Login):
    try:
        user = User.find(login.email)
        if user.verify_password(login.password):
            return signJWT(user.email, type=user.user_type)
        else:
            raise HTTPException(status_code=401, detail="Invalid email or password")
    except:
        raise HTTPException(status_code=401, detail="Invalid email or password")

# Register
class Register(BaseModel):
    name: str
    email: str
    password: str
    phone_number: str
    address: str

@router.post("/register", tags=["user"])
async def register_user(register: Register):
    user = User.new(
        register.name,
        register.email,
        register.password,
        register.phone_number,
        register.address,
        1
    )
    # user is int
    if (type(user) == int):
        if (user == 1062):
            raise HTTPException(status_code=409, detail="Email already exists")
        else:
            raise HTTPException(status_code=500, detail="Internal server error")
    return signJWT(register.email)
