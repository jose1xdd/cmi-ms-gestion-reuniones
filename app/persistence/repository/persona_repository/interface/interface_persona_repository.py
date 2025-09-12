from abc import ABC
from app.persistence.models.persona import Persona
from app.persistence.repository.base_repository.interface.ibase_repository import IBaseRepository


class IPersonaRepository(IBaseRepository[Persona, str], ABC):
    pass
