from fastapi import APIRouter, HTTPException, Depends, Header

from auth.jwt_handler import decodeJWT
from auth.jwt_bearer import JWTBearer
from database.book import Book

router = APIRouter(
    prefix="/book/loan"
)


# Loan book
@router.get("/loan", dependencies=[Depends(JWTBearer())], tags=["loan"])
async def loan_book(
        book_id: str,
        copy_id: str,
        Authorization: str | None = Header(default=None)
    ):
    # Get user email from token
    token_data = decodeJWT(token=Authorization.split(" ")[1])
    email = token_data["email"]

    #TODO Store loan in database to be approved by librarian
    # return Book.loan_book(book_id, copy_id, email)
    # errors: book not found, copy not available, user has already loaned too many books
    return {
        "isbn": "",
        "title": "",
        "loan_date": "",
        "devolution_date": "",
    }

@router.get("/return", dependencies=[Depends(JWTBearer())], tags=["loan"])
async def return_book(
        loan_id: str,
        Authorization: str | None = Header(default=None)
    ):

    # Check if user is employee
    token_data = decodeJWT(token=Authorization.split(" ")[1])
    user_type = token_data["type"]
    if (user_type == 1):
        raise HTTPException(status_code=401, detail="Unauthorized")

    #TODO Add to the tb_loan the devolution date
    return {
        "isbn": "",
        "loan_date": "",
        "devolution_date": "",
    }

# Authorized to Employees
#TODO Authorize loan
