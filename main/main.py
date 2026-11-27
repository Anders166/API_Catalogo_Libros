#Incompleto -______-
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Book
from schemas import BookCreate, BookResponse

# Crear la tabla en Neon si todavía no existe
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Books API")


# ====================================
# GET: Consultar todos los libros -done
# ====================================
@app.get("/books", response_model=list[BookResponse])
def get_book(db: Session = Depends(get_db)):
    book = db.query(Book).all()
    return book


# ====================================
# GET: Consultar un libro -done
# ====================================
@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    book = db.query(Book).filter(
        Book.id == book_id
    ).first()

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return book


# ====================================
# POST: Registrar una persona -done
# ====================================
@app.post("/books", response_model=BookResponse, status_code=201)
def create_book(
    data: BookCreate,
    db: Session = Depends(get_db)
):

    book = Book(
        title=data.title,
        author=data.author,
        publisher=data.publisher,
        year=data.year,
        category=data.category
    )

    db.add(book)
    db.commit()
    db.refresh(book)

    return book


# ====================================
# PUT: Actualizar info -done
# ====================================
@app.put("/books/{book_id}", response_model=BookResponse)
def update_person(
    book_id: int,
    data:  BookCreate,
    db: Session = Depends(get_db)
):
    book = db.query(Book).filter(
        Book.id == book_id
    ).first()

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    book.name = data.name
    book.title = data.title
    book.publisher = data.publisher
    book.year = data.year
    book.category = data.category

    db.commit()
    db.refresh(book)

    return book


# ====================================
# DELETE: Eliminar un libro -done
# ====================================
@app.delete("/books/{book_id}")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    book = db.query(Book).filter(
        Book.id == book_id
    ).first()

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    db.delete(book)
    db.commit()

    return {
        "message": "The book was successfully deleted"
    }