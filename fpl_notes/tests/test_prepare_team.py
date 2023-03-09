import pytest
from django.urls import reverse
from notes.forms import AddPlayers
from notes.models import Season, Team


@pytest.fixture
def user(django_user_model):
    user = django_user_model.objects.create_user(
        username="kiruk24", password="abcd5678"
    )
    return user


@pytest.fixture
def login_client(client, user):
    client.login(username="kiruk24", password="abcd5678")
    return client


@pytest.mark.django_db
def test_create_team(login_client):
    data = {
        "team_name": "FC SPARTAK",
    }
    url = reverse("create_team")
    response = login_client.post(url, data, follow=True)
    team_count = Team.objects.count()
    assert response.status_code == 200
    assert team_count == 1


@pytest.fixture
def fixture_add_team(login_client):
    data = {
        "team_name": "FC SPARTAK",
    }
    url = reverse("create_team")
    login_client.post(url, data, follow=True)
    team = Team.objects.get(team_name="FC SPARTAK")
    return team


@pytest.mark.django_db
def test_add_season(login_client, fixture_add_team):
    url = reverse("add_season")
    data = {
        "season_start": 2024,
        "season_end": 2025,
    }
    response = login_client.post(url, data, follow=True)
    assert response.status_code == 200
    season_count = Season.objects.count()
    assert season_count == 1
