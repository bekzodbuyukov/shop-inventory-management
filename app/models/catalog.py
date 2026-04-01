from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from app.models.base import Base

class Catalog(Base):
    __tablename__ = "catalogs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    products: Mapped[List["Product"]] = relationship("Product", back_populates="catalog", cascade="all, delete-orphan")
