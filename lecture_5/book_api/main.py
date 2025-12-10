from typing import Annotated

from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel, Field, ConfigDict, field_validator

from sqlalchemy import select, delete, update, func, Integer
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

import uvicorn

app = FastAPI() # Initialize FastAPI application

engine = create_async_engine('sqlite+aiosqlite:///books.db') # Async SQLite engine

new_session = async_sessionmaker(engine, expire_on_commit=False) # Session factory


async def get_session():
    # Provide DB session for each request
    async with new_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

class Base(DeclarativeBase):
    pass

class BookModel(Base):
    __tablename__ = "books"
    # ORM model representing a book in the database
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str]
    author: Mapped[str]
    year: Mapped[int | None]

class BookAddSchema(BaseModel):
    # ORM model representing a book data to enter
    title: str = Field(min_length=1, max_length= 50)
    author: str = Field(min_length=1, max_length= 30)
    year: int | None = Field(default=None, ge=0)


class BookSchema(BookAddSchema):
    id: int


@app.post("/setup_database")
async def setup_database():
    # Recreate tables — for testing purposes
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        return {"success": True}


@app.post("/books", response_model=BookSchema)
async def add_book(book: BookAddSchema, session: SessionDep) -> BookSchema:
    # Add a new book into the database
    new_book = BookModel(
        title=book.title,
        author=book.author,
        year=book.year,
    )
    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)
    return BookSchema(id=new_book.id, title=new_book.title, author=new_book.author, year=new_book.year)


@app.get("/books")
async def get_books(session: SessionDep,
                    limit: int = Query(10, ge=1, le=100),
                    offset: int = Query(0, ge=0),
                    ):
    # Return list of all books
    query = select(BookModel).limit(limit).offset(offset)
    result = await session.execute(query)
    books = result.scalars().all()
    if not books:
        return "There are no books."
    return [BookSchema(id=b.id, title=b.title, author=b.author, year=b.year) for b in books]

@app.delete("/books/{book_id}")
async def delete_book(book_id: int, session: SessionDep):
    # Delete a book by ID
    query = delete(BookModel).where(BookModel.id == book_id)
    result = await session.execute(query)
    await session.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"success": "Book successfully deleted"}

@app.get("/books/search")
async def get_book(session: SessionDep,
                   title: str | None = Query(default=None),
                   author: str | None = Query(default=None),
                   year: int | None = Query(default=None)):
    query = select(BookModel)
    # Flexible search — match by title/author/year
    conditions = []
    if title:
        conditions.append(func.lower(BookModel.title) == title.lower())
    if author:
        conditions.append(func.lower(BookModel.author) == author.lower())
    if year is not None:
        conditions.append(BookModel.year == year)

    if conditions:
        query = query.where(*conditions)

    result = await session.execute(query)
    books = result.scalars().all()
    if not books:
        raise HTTPException(status_code=404, detail="Book not found")

    return books

@app.put("/books/{book_id}")
async def change_book(book_id: int, session: SessionDep,
                   title: str | None = Query(default=None),
                   author: str | None = Query(default=None),
                   year: int | None = Query(default=None)):
    # Update book details by ID
    values = {}
    if title is not None:
        values["title"] = title
    if author is not None:
        values["author"] = author
    if year is not None:
        values["year"] = year

    if not values:
        raise HTTPException(status_code=400, detail="Bad Request")

    query = update(BookModel).where(BookModel.id == book_id).values(**values)
    result = await session.execute(query)
    await session.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    # Return updated book
    row = await  session.execute(select(BookModel).where(BookModel.id == book_id))
    book = row.scalar_one()
    return BookSchema(id=book.id, title=book.title, author=book.author, year=book.year)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)