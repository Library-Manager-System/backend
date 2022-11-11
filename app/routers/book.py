from fastapi import APIRouter, HTTPException

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
@router.get("/search")
async def search_books(query: str):
    #TODO search for books in database
    data = [
        {
            "title":query, "author":query, "isbn": 1
        },
        {
            "title":"title", "author":"author", "isbn": 2
        }
    ]
    return data


# Get book by isbn
@router.get("/isbn")
async def search_isbn(isbn: int):
    #TODO get book by isbn in database
    data = {
        "isbn": isbn,
        "title": "title_book",
        "author": "author_book",
        "publisher": "publisher",
        "year": 2022,
        "synopsis": "synopsis",
        "category": "category"
    }
    return data