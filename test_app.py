from app import app


def test_home_page():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Employee Management System" in response.data


def test_add_employee():
    client = app.test_client()
    response = client.post(
        "/add",
        data={"name": "Test Employee", "role": "Developer"}
    )
    assert response.status_code == 302
    assert any(e["name"] == "Test Employee" for e in app.employees)


def test_delete_employee():
    client = app.test_client()
    app.employees.append(
        {"id": 999, "name": "Delete Test", "role": "Tester"}
    )
    response = client.get("/delete/999")
    assert response.status_code == 302
    assert not any(e["id"] == 999 for e in app.employees)