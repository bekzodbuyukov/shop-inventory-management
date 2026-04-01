from fastapi.testclient import TestClient

def test_create_product(client: TestClient):
    response = client.post(
        "/api/v1/products/",
        json={"name": "Laptop", "sku": "LPT-001", "price": "999.99", "description": "Powerful laptop"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Laptop"
    assert data["sku"] == "LPT-001"
    assert "id" in data

def test_assign_product_to_catalog(client: TestClient):
    # Create catalog
    catalog_resp = client.post("/api/v1/catalogs/", json={"name": "Computers"})
    catalog_id = catalog_resp.json()["id"]
    
    # Create product
    product_resp = client.post(
        "/api/v1/products/",
        json={"name": "Mouse", "sku": "MSE-001", "price": "25.00"},
    )
    product_id = product_resp.json()["id"]
    
    # Assign
    assign_resp = client.post(f"/api/v1/products/{product_id}/assign/{catalog_id}")
    assert assign_resp.status_code == 200
    assert assign_resp.json()["catalog_id"] == catalog_id

def test_filter_products_by_catalog(client: TestClient):
    # Setup
    cat1 = client.post("/api/v1/catalogs/", json={"name": "Cat 1"}).json()["id"]
    cat2 = client.post("/api/v1/catalogs/", json={"name": "Cat 2"}).json()["id"]
    
    client.post("/api/v1/products/", json={"name": "P1", "sku": "P1", "price": "10", "catalog_id": cat1})
    client.post("/api/v1/products/", json={"name": "P2", "sku": "P2", "price": "10", "catalog_id": cat1})
    client.post("/api/v1/products/", json={"name": "P3", "sku": "P3", "price": "10", "catalog_id": cat2})
    
    # Test filtering
    response = client.get(f"/api/v1/products/?catalog_id={cat1}")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_create_duplicate_product_sku(client: TestClient):
    client.post("/api/v1/products/", json={"name": "P1", "sku": "DUPE-SKU", "price": "10"})
    response = client.post("/api/v1/products/", json={"name": "P2", "sku": "DUPE-SKU", "price": "20"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Product with this SKU already exists"

def test_create_product_invalid_catalog(client: TestClient):
    response = client.post(
        "/api/v1/products/",
        json={"name": "P1", "sku": "P1", "price": "10", "catalog_id": 9999}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Catalog not found"

def test_assign_product_invalid_catalog(client: TestClient):
    # Create product
    product_resp = client.post(
        "/api/v1/products/",
        json={"name": "Mouse", "sku": "MSE-999", "price": "25.00"},
    )
    product_id = product_resp.json()["id"]
    
    # Assign to non-existent catalog
    response = client.post(f"/api/v1/products/{product_id}/assign/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Catalog not found"
