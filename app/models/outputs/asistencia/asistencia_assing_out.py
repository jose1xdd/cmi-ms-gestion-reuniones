from typing import List
from pydantic import BaseModel

class PersonaNoAsignada(BaseModel):
    persona_id: str
    motivo: str

class AsignacionAsistenciaResponse(BaseModel):
    reunion_id: int
    personas_asignadas: List[str]
    personas_no_asignadas: List[PersonaNoAsignada]
    total_asignadas: int
    total_no_asignadas: int
