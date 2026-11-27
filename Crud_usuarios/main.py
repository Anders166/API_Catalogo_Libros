from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Person
from schemas import PersonCreate, PersonResponse

# Crear la tabla en Neon si todavía no existe
Base.metadata.create_all(bind=engine)

app = FastAPI(title="People API")


# ====================================
# GET: Consultar todas las personas
# ====================================
@app.get("/people", response_model=list[PersonResponse])
def get_people(db: Session = Depends(get_db)):
    people = db.query(Person).all()
    return people


# ====================================
# GET: Consultar una persona
# ====================================
@app.get("/people/{person_id}", response_model=PersonResponse)
def get_person(
    person_id: int,
    db: Session = Depends(get_db)
):
    person = db.query(Person).filter(
        Person.id == person_id
    ).first()

    if person is None:
        raise HTTPException(
            status_code=404,
            detail="Person not found"
        )

    return person


# ====================================
# POST: Registrar una persona
# ====================================
@app.post("/people", response_model=PersonResponse, status_code=201)
def create_person(
    data: PersonCreate,
    db: Session = Depends(get_db)
):
    # Validar que el correo no esté registrado
    existing = db.query(Person).filter(
        Person.email == data.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    person = Person(
        name=data.name,
        email=data.email,
        age=data.age
    )

    db.add(person)
    db.commit()
    db.refresh(person)

    return person


# ====================================
# PUT: Actualizar una persona
# ====================================
@app.put("/people/{person_id}", response_model=PersonResponse)
def update_person(
    person_id: int,
    data: PersonCreate,
    db: Session = Depends(get_db)
):
    person = db.query(Person).filter(
        Person.id == person_id
    ).first()

    if person is None:
        raise HTTPException(
            status_code=404,
            detail="Person not found"
        )

    # Validar que el correo no pertenezca a otra persona
    duplicated = db.query(Person).filter(
        Person.email == data.email,
        Person.id != person_id
    ).first()

    if duplicated:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    person.name = data.name
    person.email = data.email
    person.age = data.age

    db.commit()
    db.refresh(person)

    return person


# ====================================
# DELETE: Eliminar una persona
# ====================================
@app.delete("/people/{person_id}")
def delete_person(
    person_id: int,
    db: Session = Depends(get_db)
):
    person = db.query(Person).filter(
        Person.id == person_id
    ).first()

    if person is None:
        raise HTTPException(
            status_code=404,
            detail="Person not found"
        )

    db.delete(person)
    db.commit()

    return {
        "message": "Person deleted successfully"
    }