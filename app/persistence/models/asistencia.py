from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base
from app.persistence.models.persona import Persona


class Asistencia(Base):
    __tablename__ = "Asistencia"

    asistenteId = Column(String(255), ForeignKey(
        "Persona.id"), primary_key=True)
    reunionId = Column(Integer, ForeignKey("Reunion.id"), primary_key=True)
    participacion = Column(Boolean, nullable=True)

    # Relaciones
    reunion = relationship("Reunion", back_populates="asistencias")
    persona = relationship(Persona, back_populates="asistencias")
