from fastapi import APIRouter, HTTPException, Path, Query
from typing import List
from app.dependencies import DbSession
from app.schemas.catalog import CatalogCreate, CatalogUpdate, CatalogRead
from app.services.catalog_service import CatalogService

router = APIRouter(prefix="/catalogs", tags=["Catalogs"])

@router.get("/", response_model=List[CatalogRead])
def get_catalogs(db: DbSession):
    return CatalogService.get_all(db)

@router.get("/{id}", response_model=CatalogRead)
def get_catalog(db: DbSession, id: int = Path(..., gt=0)):
    db_catalog = CatalogService.get_by_id(db, id)
    if not db_catalog:
        raise HTTPException(status_code=404, detail="Catalog not found")
    return db_catalog

@router.post("/", response_model=CatalogRead, status_code=201)
def create_catalog(db: DbSession, catalog_in: CatalogCreate):
    if CatalogService.get_by_name(db, catalog_in.name):
        raise HTTPException(status_code=400, detail="Catalog with this name already exists")
    return CatalogService.create(db, catalog_in)

@router.put("/{id}", response_model=CatalogRead)
def update_catalog(db: DbSession, catalog_in: CatalogUpdate, id: int = Path(..., gt=0)):
    db_catalog = CatalogService.get_by_id(db, id)
    if not db_catalog:
        raise HTTPException(status_code=404, detail="Catalog not found")
    
    if catalog_in.name and catalog_in.name != db_catalog.name:
        if CatalogService.get_by_name(db, catalog_in.name):
            raise HTTPException(status_code=400, detail="Catalog with this name already exists")
            
    return CatalogService.update(db, db_catalog, catalog_in)

@router.delete("/{id}", status_code=204)
def delete_catalog(db: DbSession, id: int = Path(..., gt=0)):
    db_catalog = CatalogService.get_by_id(db, id)
    if not db_catalog:
        raise HTTPException(status_code=404, detail="Catalog not found")
    CatalogService.delete(db, db_catalog)
    return None
