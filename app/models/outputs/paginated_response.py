from typing import List
from pydantic import BaseModel

from app.models.outputs.reunion.reunion_out import ReunionOut


class PaginatedReunion(BaseModel):
    total_items: int
    current_page: int
    total_pages: int
    items: List[ReunionOut]
