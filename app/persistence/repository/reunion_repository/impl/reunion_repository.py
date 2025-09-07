from typing import Any, Dict
from requests import Session
from sqlalchemy import and_
from app.models.outputs.paginated_response import PaginatedReunion
from app.persistence.models.reunion import Reunion
from app.persistence.repository.base_repository.impl.base_repository import BaseRepository
from app.persistence.repository.reunion_repository.interface.interface_reunion_repository import IReunionRepository


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

    def find_all_reunion(self, page: int, page_size: int, filters: Dict[str, Any]) -> PaginatedReunion:
        query = (
            self.apply_filters(self.db, Reunion, filters)
        )
        return self.paginate(page, page_size, query)
