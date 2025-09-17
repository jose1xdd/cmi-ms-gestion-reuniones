from sqlalchemy import Boolean, Enum, Column, ForeignKey, String, Integer, Date
from app.config.database import Base
from sqlalchemy.orm import relationship

from app.persistence.models.enum import EnumDocumento, EnumEscolaridad, EnumParentesco, EnumSexo



class Persona(Base):
    __tablename__ = 'Persona'
    
    id = Column(String(36), primary_key=True)
    tipoDocumento = Column(Enum(EnumDocumento))
    nombre = Column(String(50))
    apellido = Column(String(50))
    fechaNacimiento = Column(Date)
    parentesco = Column(Enum(EnumParentesco))
    sexo = Column(Enum(EnumSexo))
    profesion = Column(String(100), nullable=True)
    escolaridad = Column(Enum(EnumEscolaridad))
    direccion = Column(String(200))
    telefono = Column(String(20))
    activo = Column(Boolean, default=True, nullable=False)
    idFamilia = Column(Integer, ForeignKey('Familia.id'))
    idParcialidad = Column(Integer, ForeignKey('Parcialidad.id'))

    asistencias = relationship("Asistencia", back_populates="persona", cascade="all, delete-orphan")
    usuario = relationship("Usuario", back_populates="persona", uselist=False)
