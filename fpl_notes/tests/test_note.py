import pytest
from django.urls import reverse
from notes.forms import AddPlayers
from notes.models import Note, Player, Season, Team


@pytest.fixture
def myuser(django_user_model):
    user = django_user_model.objects.create_user(
        username="kiruk24", password="abcd5678"
    )
    return user


@pytest.fixture
def login_client_note(client, myuser):
    client.login(username="kiruk24", password="abcd5678")
    return client


@pytest.fixture
@pytest.mark.django_db
def team(myuser):
    team = Team.objects.create(team_name="FC ABC", owner=myuser)
    team.save()
    return team


@pytest.fixture
@pytest.mark.django_db
def season(team):
    season = Season.objects.create(season_start="2024", season_end="2025", team=team)
    season.save()
    return season


@pytest.fixture
@pytest.mark.django_db
def player(team, season):
    player = Player.objects.create(
        player="Salah",
        position="MD",
        season=season,
        team=team,
    )
    player.save()
    return player


@pytest.mark.django_db
def test_get(login_client_note, team, season, player):
    url = reverse("notes")
    data = {
        "tour": 1,
        "note": "test",
        "substatution_off": player.id,
        "substatution_on": "Mane",
        "slug": "1-2024",
    }
    login_client_note.post(url, data, follow=True)
    note_count = Note.objects.count()
    assert note_count == 1


@pytest.fixture
def notee(team, season, player):
    note = Note.objects.create(
        tour=1,
        note="test",
        substatution_off=player,
        substatution_on="Mane",
        season=season,
        author=team,
        slug="1-2024",
    )
    note.save()
    return note


def test_upd_note(login_client_note, team, season, player, notee):
    url = reverse("note_update", kwargs={"slug": "1-2024"})
    notee = Note.objects.get(tour=1)
    assert notee.note == "test"
    data = {
        "tour": 1,
        "note": "test1",
        "substatution_off": player.id,
        "substatution_on": "Mane",
        "slug": "1-2024",
    }
    login_client_note.post(url, data)
    notee = Note.objects.get(tour=1)
    assert notee.note == "test1"


def test_substatution(login_client_note, team, season, player, notee):
    url = reverse("accept_sub", kwargs={"slug": "1-2024"})
    data = {
        "substatution_off": player.id,
        "substatution_on": "Mane",
    }
    login_client_note.post(url, data)
    player = Player.objects.get(player="Mane")
    player_count = Player.objects.count()
    assert player.player == "Mane"
    assert player_count == 1


def test_player_form(season):
    data = {"player": "Pope", "position": "GK", "season": season.id}
    form = AddPlayers(data=data)
    assert form.is_valid() == True
