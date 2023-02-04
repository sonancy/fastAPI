from fastapi import FastAPI, HTTPException, Request, status, Form, Header
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID
from starlette.responses import JSONResponse

app = FastAPI()


class NegativeNumberException(Exception):
    def __init__(self, books_to_return):
        self.books_to_return = books_to_return


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1, max_length=100)
    author: str = Field(min_length=1, max_length=20)
    description: Optional[str] = Field(None, min_length=1, max_length=200)
    ratings: int = Field(gt=-1, lt=11)

    class Config:
        schema_extra = {
            "example": {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "title": "Attack on Titan",
                "author": "Eren Jaeger",
                "description": "Hello world!",
                "ratings": 9
            }
        }


class NoRatingBook(BaseModel):
    id: UUID
    title: str = Field(min_length=1, max_length=100)
    author: str = Field(min_length=1, max_length=20)
    description: Optional[str] = Field(None, min_length=1, max_length=200)


BOOKS = []


@app.get('/')
async def getAllBooks(books_to_return: Optional[int] = None):
    if books_to_return and books_to_return < 0:
        raise NegativeNumberException(books_to_return=books_to_return)
    if books_to_return and len(BOOKS) >= books_to_return > 0:
        i = 0
        newBooks = []
        while i < books_to_return:
            newBooks.append(BOOKS[i])
            i += 1
        return newBooks
    return BOOKS


@app.get('/{id}')
async def getBookById(id: UUID):
    counter = 0
    for book in BOOKS:
        if book.id == id:
            return BOOKS[counter]
        counter += 1
    raise raise_404_exception()


@app.get('/ratings/{id}', response_model=NoRatingBook)
async def getBookByIdWithNoRatings(id: UUID):
    counter = 0
    for book in BOOKS:
        if book.id == id:
            return BOOKS[counter]
        counter += 1
    raise raise_404_exception()


@app.post('/', status_code=status.HTTP_201_CREATED)
async def createBook(book: Book):
    BOOKS.append(book)
    return book


@app.post('/login')
async def login(id: int, username: str = Header(None), password: str = Header(None)):
    if username == 'FastAPIUser' and password == 'test1234!':
        return BOOKS[id]
    else:
        return "Invalid User!"


@app.put('/{id}')
async def updateBook(id: UUID, book: Book):
    counter = 0
    for i in BOOKS:
        if i.id == id:
            BOOKS[counter] = book
            return BOOKS[counter]
        counter += 1
    raise raise_404_exception()


@app.delete('/{id}')
async def deleteBook(id: UUID):
    counter = 0
    for i in BOOKS:
        if i.id == id:
            del BOOKS[counter]
            return 'Deleted!'
        counter += 1
    raise raise_404_exception()


def raise_404_exception():
    raise HTTPException(status_code=404, detail="Book not Found!", headers={
                        'X-Header-Error': 'Book not found with provided UUID'})


@app.exception_handler(NegativeNumberException)
def negative_number_exception_handler(request: Request, exception: NegativeNumberException):
    return JSONResponse(
        status_code=418,
        content={"Message": f"WHY {exception.books_to_return} BOOKS!"}
    )
