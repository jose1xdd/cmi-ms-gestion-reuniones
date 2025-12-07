from pydantic import BaseModel, EmailStr


class UserRegisterAsistencia(BaseModel):
    numero_documento: str
    correo_electronico: EmailStr
