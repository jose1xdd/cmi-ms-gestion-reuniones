from typing import List
from pydantic import BaseModel

from app.models.outputs.asistencia.asistencia_out import PersonaAsistenciaOut
from app.models.outputs.reunion.reunion_out import ReunionOut


class PaginatedReunion(BaseModel):
    total_items: int
    current_page: int
    total_pages: int
    items: List[ReunionOut]


class PaginatedAsistenciaPersonas(BaseModel):
    personas_presentes: int
    personas_ausentes: int
    total_items: int
    current_page: int
    total_pages: int
    items: List[PersonaAsistenciaOut]
