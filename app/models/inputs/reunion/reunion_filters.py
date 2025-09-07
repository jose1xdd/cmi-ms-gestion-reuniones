from pydantic import BaseModel
from datetime import date, time
from typing import Optional

class ReunionFilter(BaseModel):
    titulo: Optional[str] = None
    fecha: Optional[date] = None
    horaInicio: Optional[time] = None
    horaFinal: Optional[time] = None