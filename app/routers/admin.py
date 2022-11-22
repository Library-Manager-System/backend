from fastapi import APIRouter, HTTPException, Depends

from auth.jwt_handler import signJWT
from auth.jwt_bearer import JWTBearer
from database.user import User

router = APIRouter(
    prefix="/admin"
)

# First access
first_access_accessd = False

@router.get("/first-access", tags=["admin"])
async def first_access():
    global first_access_accessd
    if first_access_accessd:
        raise HTTPException(status_code=404, detail="Not Found")
    first_access_accessd = True
    # Check if there is any user in the database
    if (User.count() == 0):
        return {
            "msg": "Use the following token to:    1) Create the first admin    2) Confirm the first admin    3) Give the first admin the maximum permission    Ps.:(this token will be invalid after one hour)",
            "access_token": signJWT("admin", permission_level=3)["access_token"]
        }
    raise HTTPException(status_code=404, detail="Not Found")


# Set User type
@router.put("/set-user-type", dependencies=[Depends(JWTBearer(min_permission=3))], tags=["admin"])
async def set_user_type(email: str, type: int):
    # Check if user exists
    try:
        user = User.find(email)
        # invalid type
        try:
            user.set_type(type)
        except:
            raise HTTPException(status_code=400, detail="Invalid type")
        return user
    except IndexError:
        raise HTTPException(status_code=404, detail="User not found")


# @router.get("/", tags=["admin"])
# async def read_admin():
#     return {
#         "username": "admin"
#     }


# # Login
# class Login(BaseModel):
#     username: str
#     password: str

# @router.post("/login", tags=["admin"])
# async def login_admin(login: Login):
#     # TODO - Check if admin exists in database
#     if login.username == "test" and login.password == "test":
#         return signJWT(login.username)
#     else:
#         raise HTTPException(status_code=401, detail="Invalid username or password")
