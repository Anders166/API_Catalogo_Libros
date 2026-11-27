from pydantic import BaseModel, ConfigDict, EmailStr, Field


# Esquema para registrar o actualizar una persona
class PersonCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    age: int = Field(gt=0)


# Esquema para devolver una persona
class PersonResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int

    model_config = ConfigDict(from_attributes=True)