from abc import ABC, abstractmethod
from typing import Optional

from app.persistence.models.asistencia import Asistencia
from app.persistence.repository.base_repository.interface.ibase_repository import IBaseRepository


class IAsistenciaRepository(IBaseRepository[Asistencia, int], ABC):
    @abstractmethod
    def get_by_reunion_and_persona(self, reunion_id: int, persona_id: int) -> Optional[Asistencia]:
        pass
