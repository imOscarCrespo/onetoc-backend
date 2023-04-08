import pytest
from rest_framework.test import APIClient

from api.models import Team, Club, TabType, Tab

client = APIClient()

def return_user_access_token():
    register_payload = {
        "username": "testusercreated",
        "email": "test@test.es",
        "password": "hsaliekda23",
        "repeatedPassword": "hsaliekda23",
        "firstName": "test",
        "lastName": "test"
    }
    client.post("/register", register_payload)
    login_payload = {
        "username": "testusercreated",
        "password": "hsaliekda23",
    }
    response = client.post("/api/token/", login_payload)
    return response.data['access']


@pytest.mark.django_db
def test_register_user():
    access_token = return_user_access_token()
    club_count = Club.objects.count()
    team_count = Team.objects.count()
    tab_count = Tab.objects.count()
    tab_type_count = TabType.objects.count()
    headers = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
    if club_count == 0:
        payload = {
            'name': 'test'
        }
        client.post("/club", payload, **headers)
    if team_count == 0:
        club = Club.objects.get()
        payload = {
            'name': 'test',
            'club_name': 'test'
        }
        client.post("/team", payload, **headers)
    if tab_type_count == 0:
        payload = {
            'name': 'test'
        }
        response = client.post("/tabType", payload, **headers)
    if tab_count == 0:
        tab_type = TabType.objects.get()
        payload = {
            'name': 'test',
            'icon': 'test',
            'order': 1,
            'type': tab_type.pk,
        }
        response = client.post("/tab", payload, **headers)
    team = Team.objects.get()
    tab = Tab.objects.get()
    payload = {
        'name': 'test',
        'timeline': '',
        'status': 'PUBLISHED',
        'team': team.pk,  # team id
        'media': '',
        'tab': tab.pk  # tab id
    }

    response = client.post("/match", payload, **headers)
    data = response.data
    assert data["name"] == payload["name"]