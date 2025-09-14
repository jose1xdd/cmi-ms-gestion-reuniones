from pydantic import BaseModel

class PersonaAsistenciaOut(BaseModel):
    Numero_documento: str
    Nombre: str
    Apellido: str
    Asistencia: bool

    class Config:
        from_attributes = True  # Permite mapear desde SQLAlchemy