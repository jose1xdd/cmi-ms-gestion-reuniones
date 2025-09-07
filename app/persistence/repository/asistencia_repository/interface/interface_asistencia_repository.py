from abc import ABC, abstractmethod

from app.persistence.models.asistencia import Asistencia
from app.persistence.repository.base_repository.interface.ibase_repository import IBaseRepository


class IAsistenciaRepository(IBaseRepository[Asistencia, int], ABC):
    pass
