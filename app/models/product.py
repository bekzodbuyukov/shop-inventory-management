from sqlalchemy import String, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal
from typing import Optional
from app.models.base import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    sku: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    catalog_id: Mapped[Optional[int]] = mapped_column(ForeignKey("catalogs.id", ondelete="SET NULL"), nullable=True)
    catalog: Mapped[Optional["Catalog"]] = relationship("Catalog", back_populates="products")
