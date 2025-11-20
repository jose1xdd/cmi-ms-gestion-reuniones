from datetime import date, time
from enum import Enum
from typing import Optional
from pydantic import BaseModel

class EnumEstadoActividad(str, Enum):
    PROGRAMADA = "PROGRAMADA"
    EN_CURSO = "EN_CURSO"
    COMPLETADA = "COMPLETADA"
    
class ReunionOut(BaseModel):
    id: int
    titulo: Optional[str] = None
    fecha: Optional[date] = None
    horaInicio: Optional[time] = None
    horaFinal: Optional[time] = None
    ubicacion: Optional[str] = None
    estado: Optional[EnumEstadoActividad] = None
    class Config:
        from_attributes = True


class ReunionesPorEstado(BaseModel):
    programadas: int
    en_curso: int
    cerradas: int
