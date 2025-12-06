from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import case, desc, func, or_
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
        query: Optional[str] = None
    ) -> PaginatedAsistenciaPersonas:

        query_str = query.strip() if query else ""

        q = (
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
            .filter(Persona.fechaDefuncion.is_(None))
            .order_by(
                desc(
                    case(
                        (Asistencia.id.isnot(None), True),
                        else_=False
                    )
                )
            )
        )

        # --- FILTRO POR QUERY (documento, nombre, apellido) ---
        if query_str:
            like_query = f"%{query_str}%"
            q = q.filter(
                or_(
                    Persona.id.like(like_query),
                    func.lower(Persona.nombre).like(func.lower(like_query)),
                    func.lower(Persona.apellido).like(func.lower(like_query)),
                )
            )

        presentes = q.filter(Asistencia.id.isnot(None)).count()
        ausentes = q.filter(Asistencia.id.is_(None)).count()

        paginated = self.paginate(page, page_size, q)

        return PaginatedAsistenciaPersonas(
            total_items=paginated['total_items'],
            current_page=paginated['current_page'],
            total_pages=paginated['total_pages'],
            items=paginated['items'],
            personas_presentes=presentes,
            personas_ausentes=ausentes
        )
