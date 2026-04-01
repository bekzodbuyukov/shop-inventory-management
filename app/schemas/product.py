from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from decimal import Decimal

class ProductBase(BaseModel):
    name: str
    sku: str
    price: Decimal = Field(max_digits=10, decimal_places=2)
    description: Optional[str] = None
    catalog_id: Optional[int] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    price: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)
    description: Optional[str] = None
    catalog_id: Optional[int] = None

class ProductRead(ProductBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
