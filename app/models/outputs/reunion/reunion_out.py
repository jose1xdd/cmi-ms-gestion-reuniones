from datetime import date, time
from typing import Optional
from pydantic import BaseModel


class ReunionOut(BaseModel):
    id: int
    titulo: Optional[str] = None
    fecha: Optional[date] = None
    horaInicio: Optional[time] = None
    horaFinal: Optional[time] = None
    ubicacion: Optional[str] = None
    editable: Optional[bool] = None
    class Config:
        from_attributes = True