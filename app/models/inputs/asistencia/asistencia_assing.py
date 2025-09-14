from typing import List
from pydantic import BaseModel


class AssingAsistencia(BaseModel):
    persona_id: List[str]
