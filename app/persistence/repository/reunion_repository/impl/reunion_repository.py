from typing import Any, Dict
from sqlalchemy import func, case, and_
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.models.outputs.reunion.reunion_out import EnumEstadoActividad
from app.persistence.models.reunion import EstadoReunion, Reunion
from app.persistence.repository.base_repository.impl.base_repository import BaseRepository
from app.persistence.repository.reunion_repository.interface.interface_reunion_repository import IReunionRepository
from app.utils.exceptions_handlers.models.error_response import AppException


class ReunionRepository(BaseRepository, IReunionRepository):
    def __init__(self, db: Session):
        super().__init__(Reunion, db)

    def contar_por_estado(self):
        query = (
            self.db.query(
                func.sum(
                    case((Reunion.estado == EstadoReunion.PROGRAMADA, 1), else_=0)
                ).label("programadas"),
                func.sum(
                    case((Reunion.estado == EstadoReunion.EN_CURSO, 1), else_=0)
                ).label("en_curso"),
                func.sum(
                    case((Reunion.estado == EstadoReunion.CERRADA, 1), else_=0)
                ).label("cerradas"),
            )
        )

        result = query.first()

        return {
            "PROGRAMADA": result.programadas or 0,
            "EN_CURSO": result.en_curso or 0,
            "CERRADA": result.cerradas or 0
        }

    def existe_conflicto_reunion(self, fecha, hora_inicio, hora_final, reunion_id: int = None) -> bool:
        query = self.db.query(Reunion).filter(
            Reunion.fecha == fecha,
            and_(
                Reunion.horaInicio < hora_final,
                Reunion.horaFinal > hora_inicio
            )
        )

        if reunion_id:
            query = query.filter(Reunion.id != reunion_id)

        return self.db.query(query.exists()).scalar()

    def find_all_reunion(self, page: int, page_size: int, filters: Dict[str, Any]):

        # Construcción base
        query = self.db.query(Reunion)

        # Aplicar filtros dinámicos solo si existen
        for field, value in filters.items():
            if value is not None:
                query = query.filter(getattr(Reunion, field) == value)

        # Orden por fecha descendente
        query = query.order_by(Reunion.fecha.desc())

        # Paginación
        paginated = self.paginate(page, page_size, query)

        # Normaliza items para salida consistente
        paginated["items"] = [
            {
                "id": row.id,
                "titulo": row.titulo,
                "fecha": row.fecha,
                "horaInicio": row.horaInicio,
                "horaFinal": row.horaFinal,
                "ubicacion": row.ubicacion,
                "estado": row.estado.value if hasattr(row.estado, "value") else row.estado,
            }
            for row in paginated["items"]
        ]

        return paginated

    def update_estado(self, reunion_id: int, nuevo_estado: EstadoReunion) -> Reunion:
        reunion = self.db.query(Reunion).filter(
            Reunion.id == reunion_id).first()

        if not reunion:
            raise AppException(f"No existe una reunión con ID {reunion_id}")

        reunion.estado = nuevo_estado
        self.db.commit()
        self.db.refresh(reunion)
        return reunion
