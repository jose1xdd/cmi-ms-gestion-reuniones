from pydantic import BaseModel


class AsistenciaIndividual(BaseModel):
    asistencia_persona: bool
    class Config:
        from_attributes = True  # Permite mapear desde SQLAlchemy