from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import case, desc
from app.models.outputs.paginated_response import PaginatedAsistenciaPersonas
from app.persistence.models.asistencia import Asistencia
from app.persistence.models.persona import Persona
from app.persistence.models.usuario import Usuario
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

    from typing import Optional

    def get_personas_with_asistencia(
        self,
        page: int,
        page_size: int,
        reunion_id: int,
        numero_documento: Optional[str] = None,
        nombre: Optional[str] = None,
        apellido: Optional[str] = None
    ) -> PaginatedAsistenciaPersonas:

        query = (
            self.db.query(
                Persona.id.label("Numero_documento"),
                Persona.nombre.label("Nombre"),
                Persona.apellido.label("Apellido"),
                case(
                    (Asistencia.id.isnot(None), True),
                    else_=False
                ).label("Asistencia")
            )
            .outerjoin(
                Asistencia,
                (Asistencia.asistenteId == Persona.id) &
                (Asistencia.reunionId == reunion_id)
            )
            .filter(Persona.fechaDefuncion == None)
            .order_by(
                desc(
                    case(
                        (Asistencia.id.isnot(None), True),
                        else_=False
                    )
                )
            )
        )

        # Aplicar filtros dinámicos
        if numero_documento:
            query = query.filter(Persona.id == numero_documento)

        if nombre:
            query = query.filter(Persona.nombre.ilike(f"%{nombre}%"))

        if apellido:
            query = query.filter(Persona.apellido.ilike(f"%{apellido}%"))

        presentes = query.filter(Asistencia.id.isnot(None)).count()
        ausentes = query.filter(Asistencia.id.is_(None)).count()

        paginated = self.paginate(page, page_size, query)

        return PaginatedAsistenciaPersonas(
            total_items=paginated['total_items'],
            current_page=paginated['current_page'],
            total_pages=paginated['total_pages'],
            items=paginated['items'],
            personas_presentes=presentes,
            personas_ausentes=ausentes)
