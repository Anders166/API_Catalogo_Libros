from sqlalchemy import Column, Integer, String

from database import Base


class Person(Base):
    # Nombre de la tabla
    __tablename__ = "people"

    # Columnas de la tabla
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    age = Column(Integer, nullable=False)