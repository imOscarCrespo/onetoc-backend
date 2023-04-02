import json

import pytest
from rest_framework.test import APIClient

client = APIClient()
@pytest.mark.django_db
def test_register_user():
    payload = {
        "username": "testusercreated",
        "email": "test@test.es",
        "password": "hsaliekda23",
        "repeatedPassword": "hsaliekda23",
        "firstName": "test",
        "lastName": "test"
    }

    response = client.post("/register", payload)
    data = response.data
    assert data["first_name"] == payload["firstName"]
    assert data["username"] == payload["username"]

@pytest.mark.django_db
def test_register_invalid_username():
    payload = {
        "username": "",
        "email": "test@test.es",
        "password": "hsaliekda23",
        "repeatedPassword": "hsaliekda23",
        "firstName": "test",
        "lastName": "test"
    }
    response = client.post("/register", payload)
    assert response.status_code == 400

@pytest.mark.django_db
def test_register_pwd_not_match():
    payload = {
        "username": "",
        "email": "test@test.es",
        "password": "hsaliekda23",
        "repeatedPassword": "hsaliekda2",
        "firstName": "test",
        "lastName": "test"
    }
    response = client.post("/register", payload)
    response_body = json.loads(response.content)
    expected_body = {"password": "Password fields didn't match."}
    assert response_body == expected_body
    assert response.status_code == 400

