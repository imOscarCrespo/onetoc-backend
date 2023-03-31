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


# @pytest.mark.django_db
# def test_login_user():
#     payload = dict(
#         username= "",
#         password="timeforsomething"
#     )
#
#     response = client.post("/api/token/", payload)
#     data = response.data
#     assert data["first_name"] == payload["first_name"]