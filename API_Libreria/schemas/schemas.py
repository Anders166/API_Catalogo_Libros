from pydantic import BaseModel, ConfigDict, EmailStr, Field


# Esquema para registrar o actualizar una persona
class BookCreate(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    author: str = Field(min_length=2, max_length=100)
    publisher: str = Field(min_length=2, max_length=100)
    year: int = Field(gt=0)
    category: str = Field(min_length=2, max_length=100)

# Esquema para devolver una persona
class BookResponse(BaseModel):
    id: int
    name: str
    email: str
    age:int

    model_config = ConfigDict(from_attributes=True)