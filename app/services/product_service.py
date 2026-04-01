from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

class ProductService:
    @staticmethod
    def get_all(db: Session, catalog_id: Optional[int] = None) -> List[Product]:
        query = select(Product)
        if catalog_id is not None:
            query = query.where(Product.catalog_id == catalog_id)
        return list(db.execute(query).scalars().all())

    @staticmethod
    def get_by_id(db: Session, product_id: int) -> Optional[Product]:
        return db.get(Product, product_id)

    @staticmethod
    def get_by_sku(db: Session, sku: str) -> Optional[Product]:
        return db.execute(select(Product).where(Product.sku == sku)).scalar_one_or_none()

    @staticmethod
    def create(db: Session, product_in: ProductCreate) -> Product:
        product = Product(**product_in.model_dump())
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def update(db: Session, db_product: Product, product_in: ProductUpdate) -> Product:
        update_data = product_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_product, field, value)
        db.commit()
        db.refresh(db_product)
        return db_product

    @staticmethod
    def delete(db: Session, db_product: Product) -> None:
        db.delete(db_product)
        db.commit()

    @staticmethod
    def assign_to_catalog(db: Session, db_product: Product, catalog_id: Optional[int]) -> Product:
        db_product.catalog_id = catalog_id
        db.commit()
        db.refresh(db_product)
        return db_product
