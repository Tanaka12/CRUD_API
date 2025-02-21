from typing import Optional
from pydantic import BaseModel

class ProductSchema(BaseModel):
    id: Optional[int] = None
    name: str
    description: str