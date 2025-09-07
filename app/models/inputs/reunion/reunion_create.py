from datetime import date, time
from typing import Optional
from pydantic import BaseModel


class ReunionCreate(BaseModel):
    titulo: str
    fecha: date
    horaInicio: time
    horaFinal: time
    class Config:
        from_attributes = True  # Para convertir entre SQLAlchemy y Pydantic fácilmente
