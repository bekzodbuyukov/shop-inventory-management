from fastapi import APIRouter, HTTPException, Path, Query
from typing import List, Optional
from app.dependencies import DbSession
from app.schemas.product import ProductCreate, ProductUpdate, ProductRead
from app.services.product_service import ProductService
from app.services.catalog_service import CatalogService

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=List[ProductRead])
def get_products(db: DbSession, catalog_id: Optional[int] = Query(None)):
    return ProductService.get_all(db, catalog_id)

@router.get("/{id}", response_model=ProductRead)
def get_product(db: DbSession, id: int = Path(..., gt=0)):
    db_product = ProductService.get_by_id(db, id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.post("/", response_model=ProductRead, status_code=201)
def create_product(db: DbSession, product_in: ProductCreate):
    if ProductService.get_by_sku(db, product_in.sku):
        raise HTTPException(status_code=400, detail="Product with this SKU already exists")
    
    if product_in.catalog_id:
        if not CatalogService.get_by_id(db, product_in.catalog_id):
            raise HTTPException(status_code=404, detail="Catalog not found")
            
    return ProductService.create(db, product_in)

@router.put("/{id}", response_model=ProductRead)
def update_product(db: DbSession, product_in: ProductUpdate, id: int = Path(..., gt=0)):
    db_product = ProductService.get_by_id(db, id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product_in.sku and product_in.sku != db_product.sku:
        if ProductService.get_by_sku(db, product_in.sku):
            raise HTTPException(status_code=400, detail="Product with this SKU already exists")
            
    if product_in.catalog_id:
        if not CatalogService.get_by_id(db, product_in.catalog_id):
            raise HTTPException(status_code=404, detail="Catalog not found")
            
    return ProductService.update(db, db_product, product_in)

@router.delete("/{id}", status_code=204)
def delete_product(db: DbSession, id: int = Path(..., gt=0)):
    db_product = ProductService.get_by_id(db, id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    ProductService.delete(db, db_product)
    return None

@router.post("/{id}/assign/{catalog_id}", response_model=ProductRead)
def assign_product_to_catalog(db: DbSession, id: int = Path(..., gt=0), catalog_id: int = Path(..., gt=0)):
    db_product = ProductService.get_by_id(db, id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if not CatalogService.get_by_id(db, catalog_id):
        raise HTTPException(status_code=404, detail="Catalog not found")
        
    return ProductService.assign_to_catalog(db, db_product, catalog_id)
