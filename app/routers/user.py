from fastapi import APIRouter, HTTPException, Depends
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
        # Get user from database
        user = User.find(login.email)
        # Check password
        if user.verify_password(login.password):
            # Check if Confirmed user
            if user.confirmed_account == 0:
                # User not confirmed
                raise HTTPException(status_code=401, detail="Account not confirmed")
            # Login Success - Return JWT
            return signJWT(user.email, permission_level=user.get_permission_level())
        else:
            # Password incorrect
            raise HTTPException(status_code=401, detail="Invalid email or password")
    except IndexError:
        # User not found
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
    return {
        "msg": "User created"
    }


# Authorized to Employees
# Confirm user
@router.put("/confirm", dependencies=[Depends(JWTBearer(min_permission=2))], tags=["admin"])
async def confirm_user(email: str):
    try:
        user = User.find(email)
        user.confirm_account()
        return {
            "msg": "User confirmed",
            "user": user.email
        }
    except IndexError:
        raise HTTPException(status_code=404, detail="User not found")
