from fastapi import FastAPI
from enum import Enum
from typing import Optional

app = FastAPI()

BOOKS = {
    'book_1': {'title': 'Attack on Titan', 'author': 'Eren Jaeger'},
    'book_2': {'title': 'One Piece', 'author': 'Monkey D. Luffy'},
    'book_3': {'title': 'Naruto: Shipudden', 'author': 'Naruto Uzumaki'},
    'book_4': {'title': 'My Hero Academia', 'author': 'Izuku Midoriya'},
    'book_5': {'title': 'HoriMiya', 'author': 'Kyouko Hori'}
}

class Directions(str, Enum):
    north = 'North'
    south = 'South'
    east = 'East'
    west = 'West'

@app.get('/')
async def getAllBooks(skip_book: Optional[str] = None):
    if skip_book:
        newBooks = BOOKS.copy()
        del newBooks[skip_book]
        return newBooks
    return BOOKS

@app.get('/{book}')
async def getBookByTitle(book: str):
    return BOOKS[book]

@app.get('/')
async def getBookByTitle(book: str):
    return BOOKS[book]

@app.post('/')
async def createBook(title, author):
    current_id = 0
    if len(BOOKS) > 0:
        for book in BOOKS:
            x = int(book.split('_')[-1])
            if x > current_id:
                current_id = x
    BOOKS[f'book_{current_id + 1}'] = {'title': title, 'author': author}
    return BOOKS[f'book_{current_id + 1}']

@app.put('/{book}')
async def updateBook(book, title, author):
    newBook = {'title': title, author: author}
    BOOKS[book] = newBook
    return BOOKS[book]

@app.delete('/{book}')
async def deleteBook(book):
    BOOKS.pop(book)
    return f'Deleted!'

@app.delete('/')
async def deleteBook(book):
    BOOKS.pop(book)
    return f'Deleted!'

@app.get('/directions/{direction}')
async def getDirection(direction: Directions):
    if direction == Directions.north:
        return {'Direction': Directions.north, 'sub': "UP"}
    if direction == Directions.south:
        return {'Direction': Directions.south, 'sub': "DOWN"}
    if direction == Directions.east:
        return {'Direction': Directions.east, 'sub': "RIGHT"}
    if direction == Directions.west:
        return {'Direction': Directions.west, 'sub': "LEFT"}