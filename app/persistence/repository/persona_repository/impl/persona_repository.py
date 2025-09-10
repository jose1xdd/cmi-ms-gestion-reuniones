from sqlalchemy.orm import Session
from app.persistence.models.persona import Persona
from app.persistence.repository.base_repository.impl.base_repository import BaseRepository
from app.persistence.repository.persona_repository.interface.interface_persona_repository import IPersonaRepository


class PersonaRepository(BaseRepository, IPersonaRepository):
    def __init__(self, db: Session):
        super().__init__(Persona, db)
