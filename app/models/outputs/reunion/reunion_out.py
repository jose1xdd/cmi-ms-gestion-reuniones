from datetime import date, time
from typing import Optional, List
from pydantic import BaseModel


class ReunionOut(BaseModel):
    id: int
    titulo: Optional[str] = None
    fecha: Optional[date] = None
    horaInicio: Optional[time] = None
    horaFinal: Optional[time] = None

    class Config:
        orm_mode = True