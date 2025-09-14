from pydantic import BaseModel


class AsistenciaIndividual(BaseModel):
    asistencia_persona: bool
