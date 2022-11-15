from fastapi import APIRouter, HTTPException, Depends

from auth.jwt_bearer import JWTBearer
from database.book import Book

router = APIRouter(
    prefix="/book"
)


# Get all books
@router.get("/", tags=["book"])
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