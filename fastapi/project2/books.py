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
    rating: int


class BookRequest(BaseModel):
    id: int | None
    title: str = Field(min_length=3)
    author: str = Field(max_length=150)
    description: str = Field(min_length=5, max_length=300)
    rating: int = Field(gt=0, lt=6)


BOOKS = [
    Book(1, "Computer Science Pro", "codingwithroby", "A very nice book", 5),
    Book(2, "Be fast with FastAPI", "codingwithroby", "This is a great book", 5),
    Book(3, "Master Endpoints", "codingwithroby", "This is a awesome book", 5),
    Book(4, "HP1", "Author 1", "Book description", 2),
    Book(5, "HP2", "Author 2", "Book description", 3),
    Book(6, "HP3", "Author 3", "Book description", 1),
]


@app.get("/books")
async def read_all_bocks():
    return BOOKS


@app.post("/books/create")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    BOOKS.append(_with_id(new_book))


def _with_id(book: Book) -> Book:
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book
