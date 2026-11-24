from sqlalchemy import Column, Integer, String

from database import Base


class Person(Base):
    # Nombre de la tabla
    __tablename__ = "Books"

    # Columnas de la tabla
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    author = Column(String(100), nullable=False)
    publisher = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)
    category = Column(String(100), nullable=False)