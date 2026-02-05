import string
from pydantic import BaseModel


class NPWithDistance(BaseModel):
    np_id: str
    distance: float