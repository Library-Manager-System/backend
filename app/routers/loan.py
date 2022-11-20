from fastapi import APIRouter, HTTPException, Depends, Header, Body
from typing import Union
from datetime import date, timedelta

from auth.jwt_handler import decodeJWT
from auth.jwt_bearer import JWTBearer
from database.loan import Loan
from database.user import User
from database.book import Book

router = APIRouter(
    prefix="/book/loan"
)


# Loan book
@router.get("/request", dependencies=[Depends(JWTBearer())], tags=["loan"])
async def request_loan_book(
        book_isbn: str,
        copy_id: str,
        date_of_collection: date = date.today(), # date format: YYYY-MM-DD
        Authorization: str | None = Header(default=None)
    ):
    # Get user email from token
    token_data = decodeJWT(token=Authorization.split(" ")[1])
    email = token_data["email"]

    user_id = User.find(email).id
    try:
        book = Book.find_book_by_isbn(book_isbn)
    except IndexError:
        raise HTTPException(status_code=404, detail="Book not found")

    date_expected_devolution_loan = date_of_collection + timedelta(days=book.limit_days_loan)

    loan = Loan.new(
        user_id,
        copy_id,
        date_of_collection,
        date.today(),
        date_expected_devolution_loan,
        False,
    )

    # errors: book not found, copy not available, user has already loaned too many books
    if (loan == 1062):
        raise HTTPException(status_code=409, detail="Book already requested")
    elif (loan == 1452):
        raise HTTPException(status_code=409, detail="Invalid id reference")
    print(loan)
    return {
        "isbn": book_isbn,
        "title": book.title_book,
        "expected_loan_date": date_of_collection,
        "expected_devolution_date": date_expected_devolution_loan,
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


@router.get("/list", dependencies=[Depends(JWTBearer())], tags=["loan"])
async def list_loans(
        email: str = None,
        Authorization: str | None = Header(default=None)
    ):
    token_data = decodeJWT(token=Authorization.split(" ")[1])
    user_type = token_data["type"]
    # Check if user is employee or if the user is requesting his own loans
    if (
        user_type == 1
        or
        email == None):
        email = token_data["email"]

    return Loan.list_user_loans(email)


# Authorized to Employees
#TODO Authorize loan
@router.get("/authorize", dependencies=[Depends(JWTBearer())], tags=["loan"])
async def authorize_loan(
        loan_id: str,
        Authorization: str | None = Header(default=None)
    ):
    # Check if user is employee
    token_data = decodeJWT(token=Authorization.split(" ")[1])
    user_type = token_data["type"]
    if (user_type == 1):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    #TODO Authorize in database the loan
    return {
        "isbn": "",
        "loan_date": "",
        "devolution_date": "",
    }

