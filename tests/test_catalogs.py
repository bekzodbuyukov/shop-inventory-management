from fastapi.testclient import TestClient

def test_create_catalog(client: TestClient):
    response = client.post(
        "/api/v1/catalogs/",
        json={"name": "Electronics", "description": "Gadgets and devices"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Electronics"
    assert "id" in data

def test_read_catalogs(client: TestClient):
    client.post("/api/v1/catalogs/", json={"name": "Catalog 1"})
    client.post("/api/v1/catalogs/", json={"name": "Catalog 2"})
    
    response = client.get("/api/v1/catalogs/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2

def test_update_catalog(client: TestClient):
    create_resp = client.post("/api/v1/catalogs/", json={"name": "Old Name"})
    catalog_id = create_resp.json()["id"]
    
    response = client.put(f"/api/v1/catalogs/{catalog_id}", json={"name": "New Name"})
    assert response.status_code == 200
    assert response.json()["name"] == "New Name"

def test_delete_catalog(client: TestClient):
    create_resp = client.post("/api/v1/catalogs/", json={"name": "Delete Me"})
    catalog_id = create_resp.json()["id"]
    
    response = client.delete(f"/api/v1/catalogs/{catalog_id}")
    assert response.status_code == 204

def test_create_duplicate_catalog(client: TestClient):
    client.post("/api/v1/catalogs/", json={"name": "Unique Name"})
    response = client.post("/api/v1/catalogs/", json={"name": "Unique Name"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Catalog with this name already exists"
