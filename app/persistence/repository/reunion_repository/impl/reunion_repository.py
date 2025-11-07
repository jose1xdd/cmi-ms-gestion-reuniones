from typing import Any, Dict
from sqlalchemy import func, case, and_
from sqlalchemy import and_
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.outputs.paginated_response import PaginatedReunion
from app.models.outputs.reunion.reunion_out import EnumEstadoActividad
from app.persistence.models.enum import EstadoReunion
from app.persistence.models.reunion import Reunion
from app.persistence.repository.base_repository.impl.base_repository import BaseRepository
from app.persistence.repository.reunion_repository.interface.interface_reunion_repository import IReunionRepository
from app.utils.exceptions_handlers.models.error_response import AppException


class ReunionRepository(BaseRepository, IReunionRepository):
    def __init__(self, db: Session):
        super().__init__(Reunion, db)

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
        now = datetime.now()

        # Usamos CASE para calcular el estado dinámicamente
        estado_case = case(
            (
                # COMPLETADA: la reunión terminó antes del momento actual
                func.timestamp(func.concat(Reunion.fecha, ' ', Reunion.horaFinal)) < now,
                EnumEstadoActividad.COMPLETADA,
            ),
            (
                # EN_CURSO: la fecha actual está entre horaInicio y horaFinal
                and_(
                    func.timestamp(func.concat(Reunion.fecha, ' ', Reunion.horaInicio)) <= now,
                    func.timestamp(func.concat(Reunion.fecha, ' ', Reunion.horaFinal)) >= now,
                ),
                EnumEstadoActividad.EN_CURSO,
            ),
            else_=EnumEstadoActividad.PROGRAMADA
        ).label("estado")

        query = (
            self.db.query(
                Reunion.id,
                Reunion.titulo,
                Reunion.fecha,
                Reunion.horaInicio,
                Reunion.horaFinal,
                Reunion.codigoAsistencia,
                Reunion.ubicacion,
                estado_case
            )
            .filter_by(**filters)
            .order_by(Reunion.fecha.desc())
        )

        paginated = self.paginate(page, page_size, query)

        # Mapeamos el resultado para salida consistente
        paginated["items"] = [
            {
                "id": row.id,
                "titulo": row.titulo,
                "fecha": row.fecha,
                "horaInicio": row.horaInicio,
                "horaFinal": row.horaFinal,
                "codigoAsistencia": row.codigoAsistencia,
                "ubicacion": row.ubicacion,
                "estado": row.estado.value if hasattr(row.estado, "value") else row.estado,
            }
            for row in paginated["items"]
        ]

        return paginated
    
    def update_estado(self, reunion_id: int, nuevo_estado: EstadoReunion) -> Reunion:
        reunion = self.db.query(Reunion).filter(Reunion.id == reunion_id).first()

        if not reunion:
            raise AppException(f"No existe una reunión con ID {reunion_id}")

        reunion.estado = nuevo_estado
        self.db.commit()
        self.db.refresh(reunion)
        return reunion