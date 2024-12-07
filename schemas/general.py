from typing import Optional
from pydantic import BaseModel


class Inform(BaseModel):
    detail: str
    field_id: Optional[int]
