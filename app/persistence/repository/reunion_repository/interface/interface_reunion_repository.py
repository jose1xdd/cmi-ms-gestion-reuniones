from abc import ABC, abstractmethod
from typing import Any, Dict

from app.models.outputs.paginated_response import PaginatedReunion
from app.persistence.models.reunion import Reunion
from app.persistence.repository.base_repository.interface.ibase_repository import IBaseRepository


class IReunionRepository(IBaseRepository[Reunion, int], ABC):
    @abstractmethod
    def existe_conflicto_reunion(self, fecha, hora_inicio, hora_final, reunion_id: int = None) -> bool:
        pass
    
    @abstractmethod
    def find_all_reunion(self, page: int, page_size: int, filters: Dict[str, Any]) -> PaginatedReunion:
        pass
