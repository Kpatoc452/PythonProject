import pytest
import asyncio
from fastapi.testclient import TestClient
from main import main_app
from core.models.db_helper import db_helper
from core.config import settings

@pytest.fixture(scope="session")
def client():
    # Переопределяем зависимость на синхронную сессию
    def override_get_session():
        async def get_async_session():
            async with db_helper.session_factory() as session:
                return session
        return asyncio.run(get_async_session())

    main_app.dependency_overrides[db_helper.session_getter] = override_get_session
    with TestClient(main_app) as client:
        yield client
    main_app.dependency_overrides.clear()


admin_auth = settings.admin_token
test_auth_user = settings.auth_user_token

# Users
def test_verify_users_me(client):
    headers = {"Authorization": f"Bearer {test_auth_user}"}
    response = client.get("/api/users/me", headers=headers)
    assert response.status_code == 200


def test_nverify_users_me(client):
    response = client.get("/api/users/me")
    assert response.status_code == 401

def test_verify_users_me_patch(client):
    headers = {"Authorization": f"Bearer {test_auth_user}"}
    response = client.patch("/api/users/me", json={"password": "test"} ,headers=headers)
    assert response.status_code == 200

def test_verify_users_id(client):
    headers = {"Authorization": f"Bearer {test_auth_user}"}
    response = client.get("/api/users/1", headers=headers)
    assert response.status_code == 403

def test_admin_users_id(client):
    headers = {"Authorization": f"Bearer {admin_auth}"}
    response = client.get("/api/users/1", headers=headers)
    assert response.status_code == 200

def test_verify_users_id_patch(client):
    headers = {"Authorization": f"Bearer {test_auth_user}"}
    response = client.patch("/api/users/1", headers=headers)
    assert response.status_code == 403

def test_admin_users_id_patch(client):
    headers = {"Authorization": f"Bearer {admin_auth}"}
    response = client.patch("/api/users/1", json={"password": "test"}, headers=headers)
    assert response.status_code == 200

def test_verify_users_id_delete(client):
    headers = {"Authorization": f"Bearer {test_auth_user}"}
    response = client.delete("/api/users/1", headers=headers)
    assert response.status_code == 403

# Products
def test_get_products(client):
    headers = {"Authorization": f"Bearer {test_auth_user}"}
    response = client.get("/api/products", headers=headers)
    assert response.status_code == 200

def test_get_products_id(client):
    headers = {"Authorization": f"Bearer {test_auth_user}"}
    response = client.get("/api/products/12", headers=headers)
    assert response.status_code == 200

def test_patch_any_products_by_user(client):
    headers = {"Authorization": f"Bearer {test_auth_user}"}
    response = client.patch("/api/products/12", json={"price": 1}, headers=headers)
    assert response.status_code == 403

def test_patch_any_products_by_admin(client):
    headers = {"Authorization": f"Bearer {admin_auth}"}
    response = client.patch("/api/products/12", json={"price": 1}, headers=headers)
    assert response.status_code == 200

# Category
def test_get_all_category(client):
    headers = {"Authorization": f"Bearer {test_auth_user}"}
    response = client.get("/api/category", headers=headers)
    assert response.status_code == 200

def test_create_category_by_user(client):
    headers = {"Authorization": f"Bearer {test_auth_user}"}
    response = client.post("/api/category", headers=headers)
    assert response.status_code == 403

def test_get_category_by_id(client):
    headers = {"Authorization": f"Bearer {test_auth_user}"}
    response = client.get("/api/category/1", headers=headers)
    assert response.status_code == 200

def test_patch_category_by_user(client):
    headers = {"Authorization": f"Bearer {test_auth_user}"}
    response = client.patch("/api/category/1", headers=headers)
    assert response.status_code == 403

def test_patch_category_by_admin(client):
    headers = {"Authorization": f"Bearer {admin_auth}"}
    response = client.patch("/api/category/1", json={"name": "technic_test"},  headers=headers)
    assert response.status_code == 200  



  













