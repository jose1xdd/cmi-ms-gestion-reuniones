from pydantic import BaseModel
from datetime import date, time
from typing import Optional


class ReunionUpdate(BaseModel):
    titulo: Optional[str] = None
    fecha: Optional[date] = None
    horaInicio: Optional[time] = None
    horaFinal: Optional[time] = None
    ubicacion: Optional[str] = None
    editable: Optional[bool] = None