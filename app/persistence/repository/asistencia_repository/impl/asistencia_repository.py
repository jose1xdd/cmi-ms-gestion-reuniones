from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import case
from app.models.outputs.paginated_response import PaginatedAsistenciaPersonas
from app.persistence.models.asistencia import Asistencia
from app.persistence.models.persona import Persona
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

    def get_personas_with_asistencia(self, page: int, page_size: int, reunion_id: int) -> PaginatedAsistenciaPersonas:
        """Obtiene todas las personas y cruza si están en asistencia de la reunión"""
        query = (
            self.db.query(
                Persona.id.label("Numero_documento"),  # 👈 alias
                Persona.nombre.label("Nombre"),
                Persona.apellido.label("Apellido"),
                case(
                    (Asistencia.id.isnot(None), True),  # ✅ corregido
                    else_=False
                ).label("Asistencia")
            )
            .outerjoin(
                Asistencia,
                (Asistencia.asistenteId == Persona.id) &
                (Asistencia.reunionId == reunion_id)
            ).filter(Persona.activo.is_(True))
        )
        return self.paginate(page, page_size, query)
