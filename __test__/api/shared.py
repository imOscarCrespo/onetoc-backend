from rest_framework.test import APIClient

from api.models import Team, Club, TabType, Tab, User

client = APIClient()
def get_http_headers():
    return headers


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


access_token = return_user_access_token()

headers = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}


def create_or_get_club():
    club_count = Club.objects.count()
    if club_count == 0:
        payload = {
            'name': 'test'
        }
        client.post("/club", payload, **headers)
    return Club.objects.get()


def create_or_get_team():
    team_count = Team.objects.count()
    if team_count == 0:
        payload = {
            'name': 'test',
            'club_name': 'test'
        }
        client.post("/team", payload, **headers)
    return Team.objects.get()


def create_or_get_tab_type():
    tab_type_count = TabType.objects.count()
    if tab_type_count == 0:
        payload = {
            'name': 'test'
        }
        client.post("/tabType", payload, **headers)
    return TabType.objects.get()


def create_or_get_tab():
    tab_count = Tab.objects.count()
    if tab_count == 0:
        tab_type = create_or_get_tab_type()
        payload = {
            'name': 'test',
            'icon': 'test',
            'order': 1,
            'type': tab_type.pk,
        }
        client.post("/tab", payload, **headers)
    return Tab.objects.get()