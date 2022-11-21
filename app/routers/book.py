from fastapi import APIRouter, HTTPException, Depends, Header

from auth.jwt_bearer import JWTBearer
from database.book import Book

router = APIRouter(
    prefix="/book"
)


# Get all books
@router.get("/", dependencies=[Depends(JWTBearer())], tags=["book"])
async def list_books():
    try:
        return Book.list_book()
    except:
        raise HTTPException(status_code=500, detail="Internal server error")


# Search for books
@router.get("/search", dependencies=[Depends(JWTBearer())], tags=["book"])
async def search_books(query: str):
    return Book.find_book_by_data(query)


# Get book by isbn
@router.get("/isbn", dependencies=[Depends(JWTBearer())], tags=["book"])
async def search_isbn(isbn: str):
    try:
        return vars(Book.find_book_by_isbn(isbn))
    except IndexError:
        raise HTTPException(status_code=404, detail="Book not found")


# Authorized to Employees
# Edit book
@router.put("/edit", dependencies=[Depends(JWTBearer(min_permission=2))], tags=["book"])
async def edit_book(
        isbn: str,
        title_book: str = None,
        limit_days_loan: int = None,
        year_book: int = None,
        synopsis_book: str = None,
        id_publisher: int = None
    ):

    # Edit book
    try:
        book = Book.edit_book(
            isbn,
            title_book,
            limit_days_loan,
            year_book,
            synopsis_book,
            id_publisher
        )
        return book
    except IndexError:
        raise HTTPException(status_code=404, detail="Book not found")
