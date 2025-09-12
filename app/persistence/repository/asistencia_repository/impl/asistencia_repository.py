from typing import Optional
from sqlalchemy.orm import Session
from app.persistence.models.asistencia import Asistencia
from app.persistence.repository.asistencia_repository.interface.interface_asistencia_repository import IAsistenciaRepository
from app.persistence.repository.base_repository.impl.base_repository import BaseRepository


class AsistenciaRepository(BaseRepository, IAsistenciaRepository):
    def __init__(self, db: Session):
        super().__init__(Asistencia, db)

    def get_by_reunion_and_persona(self, reunion_id: int, persona_id: int) -> Optional[Asistencia]:
        return (
            self.db.query(Asistencia)
            .filter(Asistencia.reunionId == reunion_id)
            .filter(Asistencia.asistenteId == persona_id)
            .first()
        )
