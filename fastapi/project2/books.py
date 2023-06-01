from dataclasses import dataclass

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


@dataclass
class Book:
    id: int
    title: str
    author: str
    description: str
    publish_date: int
    rating: int


class BookRequest(BaseModel):
    id: int | None
    title: str = Field(min_length=3)
    author: str = Field(max_length=150)
    description: str = Field(min_length=5, max_length=300)
    publish_date: int = Field()
    rating: int = Field(gt=0, lt=6)

    class Config:
        schema_extra = {
            "example": {
                "title": "A essência de tudo",
                "author": "Enzo Pedro Bonacina",
                "description": "O alicerce do raciocínio",
                "publish_date": 1994,
                "rating": 5,
            }
        }


BOOKS = [
    Book(1, "Computer Science Pro", "codingwithroby", "A very nice book", 2015, 5),
    Book(2, "Be fast with FastAPI", "codingwithroby", "This is a great book", 2016, 5),
    Book(3, "Master Endpoints", "codingwithroby", "This is a awesome book", 2017, 5),
    Book(4, "HP1", "Author 1", "Book description", 2000, 2),
    Book(5, "HP2", "Author 2", "Book description", 2001, 3),
    Book(6, "HP3", "Author 3", "Book description", 2002, 1),
]


@app.get("/books")
async def read_all_bocks():
    return BOOKS


@app.get("/books/by_id/")
async def get_book_by_id(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book


@app.get("/books/by_rating/")
async def get_books_by_rating(rating: int):
    selected_books = [b for b in BOOKS if b.rating == rating]
    return selected_books


@app.get("/books/by_date/")
async def get_books_by_date(date: int):
    selected_books = [b for b in BOOKS if b.publish_date == date]
    return selected_books


@app.post("/books/create")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    BOOKS.append(_with_id(new_book))


@app.put("/books/")
async def update_book(new_book: Book):
    for i, book in enumerate(BOOKS):
        if book.id == new_book.id:
            BOOKS[i] = new_book


@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for i, book in enumerate(BOOKS):
        if book.id == book_id:
            BOOKS.pop(i)
            return


def _with_id(book: Book) -> Book:
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


