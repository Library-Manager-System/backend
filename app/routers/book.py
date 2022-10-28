from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/book"
)

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