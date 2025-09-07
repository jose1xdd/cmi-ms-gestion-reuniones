from typing import Type, TypeVar
from sqlalchemy.orm import Session

from app.persistence.repository.asistencia_repository.impl.asistencia_repository import AsistenciaRepository
from app.persistence.repository.asistencia_repository.interface.interface_asistencia_repository import IAsistenciaRepository
from app.persistence.repository.reunion_repository.impl.reunion_repository import ReunionRepository
from app.persistence.repository.reunion_repository.interface.interface_reunion_repository import IReunionRepository


T = TypeVar("T")


class RepositoryFactory:

    def __init__(self, db: Session):
        self.db = db

    _registry: dict[Type, Type] = {
        IReunionRepository: ReunionRepository,
        IAsistenciaRepository: AsistenciaRepository
    }

    def get_repository(self, interface: Type[T]) -> T:
        impl_class = self._registry.get(interface)
        if not impl_class:
            raise ValueError(
                f"No hay implementación registrada para la interfaz: {interface}")
        # Solo pasamos db, el modelo se define en el repositorio
        return impl_class(self.db)
