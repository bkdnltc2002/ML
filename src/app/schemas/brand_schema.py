from typing import Optional, List
from pydantic import UUID4, BaseModel

class BrandSchema(BaseModel):
    brand_name: str