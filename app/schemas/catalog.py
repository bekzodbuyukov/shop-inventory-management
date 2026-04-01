from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class CatalogBase(BaseModel):
    name: str
    description: Optional[str] = None

class CatalogCreate(CatalogBase):
    pass

class CatalogUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class CatalogRead(CatalogBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
