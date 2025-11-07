from pydantic import BaseModel, EmailStr


class UserRegisterAsistencia(BaseModel):
    numero_documento: str
    nombre_completo: str
    correo_electronico: EmailStr
