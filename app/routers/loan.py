from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Union
from datetime import date, timedelta

from auth.jwt_bearer import JWTBearer
from database.loan import Loan
from database.user import User
from database.book import Book
from database.copy import Copy

router = APIRouter(
    prefix="/book/loan"
)


# Loan book
class LoanBook(BaseModel):
    isbn: str
    date_of_collection: date = date.today() # date format: YYYY-MM-DD

@router.post("/request", tags=["loan"])
async def request_loan_book(
        loan_book: LoanBook,
        token_data = Depends(JWTBearer())
    ):
    # Get user email from token
    email = token_data["email"]

    # Get coppies of book
    copies = Copy.find_all_copy_by_isbn(loan_book.isbn)
    if len(copies) == 0:
        # No copies of book
        raise HTTPException(status_code=404, detail="Book not found")

    # First copy available
    copy = next(
        (copy for copy in copies if copy.available_copy),
        None
    )
    if copy is None:
        # No copies available
        raise HTTPException(status_code=404, detail="No copies available")

    # Get user from database
    user_id = User.find(email).id
    try:
        # Get book from database
        book = Book.find_book_by_isbn(loan_book.isbn)
    except IndexError:
        # Book not found
        raise HTTPException(status_code=404, detail="Book not found")

    # Date of return
    date_expected_devolution_loan = loan_book.date_of_collection + timedelta(days=book.limit_days_loan)

    #TODO user has already loaned too many books

    # Create loan
    loan = Loan.new(
        user_id,
        copy.id,
        loan_book.date_of_collection,
        date.today(),
        date_expected_devolution_loan,
        False,
    )

    if (loan == 1062):
        # Duplicate entry
        raise HTTPException(status_code=409, detail="Book already requested")
    elif (loan == 1452):
        # Foreign key constraint
        raise HTTPException(status_code=409, detail="Invalid id reference")

    # Set copy as unavailable
    copy.change_availability(False)

    return {
        "isbn": loan_book.isbn,
        "title": book.title_book,
        "expected_loan_date": loan_book.date_of_collection,
        "expected_devolution_date": date_expected_devolution_loan,
    }

# Return book
class ReturnBook(BaseModel):
    loan_id: str

@router.post("/return", dependencies=[Depends(JWTBearer(min_permission=2))], tags=["loan"])
async def return_book(return_book: ReturnBook):

    try:
        # Get loan from database
        loan = Loan.find(return_book.loan_id)
    except IndexError:
        # Loan not found
        raise HTTPException(status_code=404, detail="Loan not found")
    loan.dt_real_devolution_loan = date.today()
    loan.devolution_loan()
    return {
        "isbn": loan.isbn,
        "loan_date": loan.dt_loan,
        "devolution_date": loan.dt_real_devolution_loan,
    }


@router.get("/list", tags=["loan"])
async def list_loans(
        email: str = None,
        token_data = Depends(JWTBearer())
    ):
    user_permission = token_data["permission"]
    # Check if user is employee or if the user is requesting his own loans
    if (
        user_permission == 1
        or
        email == None
    ):
        email = token_data["email"]

    return Loan.list_user_loans(email)


# Authorized to Employees
# Authorize loan
class AuthorizeLoan(BaseModel):
    loan_id: int

@router.post("/authorize", dependencies=[Depends(JWTBearer(min_permission=2))], tags=["loan"])
async def authorize_loan(
        authorize_loan: AuthorizeLoan,
    ):
    loan_id = authorize_loan.loan_id

    try:
        # Get loan from database
        loan = Loan.find(loan_id)
    except IndexError:
        # Loan not found
        raise HTTPException(status_code=404, detail="Loan not found")

    loan.approve_loan()

    return {
        "isbn": loan.isbn,
        "loan_date": loan.dt_loan,
        "devolution_date": loan.dt_expected_devolution_loan,
    }

@router.get("/list/all", dependencies=[Depends(JWTBearer(min_permission=2))], tags=["loan"])
async def list_all_loans():
    return Loan.list_loans()
