from sqlalchemy import Column, Integer, String, Date, Time
from sqlalchemy.orm import relationship
from app.config.database import Base


class Reunion(Base):
    __tablename__ = "Reunion"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(255), nullable=True)
    fecha = Column(Date, nullable=True)
    horaInicio = Column(Time, nullable=True)
    horaFinal = Column(Time, nullable=True)
    codigoAsistencia = Column(String(6), nullable=False)
    # Relación con asistencias
    asistencias = relationship(
        "Asistencia", back_populates="reunion", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "fecha": self.fecha.isoformat() if self.fecha else None,
            "horaInicio": self.horaInicio.isoformat() if self.horaInicio else None,
            "horaFinal": self.horaFinal.isoformat() if self.horaFinal else None,
            "codigoAsistencia": self.codigoAsistencia,
        }
