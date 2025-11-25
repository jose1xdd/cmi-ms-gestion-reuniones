from pydantic import BaseModel
from datetime import date, time
from typing import Optional

from app.persistence.models.reunion import EstadoReunion


class ReunionFilter(BaseModel):
    titulo: Optional[str] = None
    fecha: Optional[date] = None
    horaInicio: Optional[time] = None
    horaFinal: Optional[time] = None
    ubicacion: Optional[str] = None
    estado: Optional[EstadoReunion] = None
