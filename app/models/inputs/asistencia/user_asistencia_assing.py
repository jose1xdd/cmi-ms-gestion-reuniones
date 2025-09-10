from pydantic import BaseModel


class UserAssingAsistencia(BaseModel):
    codigo_asistencia: str
    persona_id: str
