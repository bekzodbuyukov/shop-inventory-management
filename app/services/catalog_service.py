from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional
from app.models.catalog import Catalog
from app.schemas.catalog import CatalogCreate, CatalogUpdate

class CatalogService:
    @staticmethod
    def get_all(db: Session) -> List[Catalog]:
        return list(db.execute(select(Catalog)).scalars().all())

    @staticmethod
    def get_by_id(db: Session, catalog_id: int) -> Optional[Catalog]:
        return db.get(Catalog, catalog_id)

    @staticmethod
    def get_by_name(db: Session, name: str) -> Optional[Catalog]:
        return db.execute(select(Catalog).where(Catalog.name == name)).scalar_one_or_none()

    @staticmethod
    def create(db: Session, catalog_in: CatalogCreate) -> Catalog:
        catalog = Catalog(**catalog_in.model_dump())
        db.add(catalog)
        db.commit()
        db.refresh(catalog)
        return catalog

    @staticmethod
    def update(db: Session, db_catalog: Catalog, catalog_in: CatalogUpdate) -> Catalog:
        update_data = catalog_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_catalog, field, value)
        db.commit()
        db.refresh(db_catalog)
        return db_catalog

    @staticmethod
    def delete(db: Session, db_catalog: Catalog) -> None:
        db.delete(db_catalog)
        db.commit()
