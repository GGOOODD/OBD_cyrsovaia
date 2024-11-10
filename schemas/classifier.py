from pydantic import BaseModel


class Query(BaseModel):
    tablename: str
    args: dict
