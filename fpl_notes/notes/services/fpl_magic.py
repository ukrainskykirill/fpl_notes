from django.http import HttpRequest, QueryDict
from django.shortcuts import get_object_or_404
from notes.models import Note, Player, Season, Team


def validation_by_position(request: HttpRequest):
    team = get_team(request)
    season = get_season(request)
    gk = (
        Player.objects.filter(season=season)
        .filter(position="GK")
        .filter(team=team)
        .count()
    )
    df = (
        Player.objects.filter(season=season)
        .filter(position="DF")
        .filter(team=team)
        .count()
    )
    md = (
        Player.objects.filter(season=season)
        .filter(position="MD")
        .filter(team=team)
        .count()
    )
    fw = (
        Player.objects.filter(season=season)
        .filter(position="FW")
        .filter(team=team)
        .count()
    )
    data = request.POST
    for i in range(0, 15):
        match data.get(f"form-{i}-position"):
            case "GK":
                gk += 1
            case "DF":
                df += 1
            case "MD":
                md += 1
            case "FW":
                fw += 1
    if any([gk > 2, df > 5, md > 5, fw > 3]):
        return False
    return True


def get_note_by_tour(request: HttpRequest, slug: str):
    season = get_season(request)
    team = get_team(request)
    note = get_object_or_404(Note, slug=slug, season=season, author=team)
    return note


def get_seasons_and_notes(request: HttpRequest, season: str | None = None):
    team = get_team(request)
    seasons_list = Season.objects.filter(team=team)
    if season:
        season = get_object_or_404(Season, season_start=season, team=team)
        notes = Note.objects.filter(season=season.id, author=team)
        return notes, seasons_list
    notes = Note.objects.filter(author=team)
    return notes, seasons_list


def substatution(data: QueryDict) -> None:
    sub_on = data.get("substatution_on")
    sub_off = data.get("substatution_off")
    player = Player.objects.get(id=sub_off)
    player.player = sub_on
    player.save()


def get_team(request: HttpRequest):
    user = request.user.id
    team = Team.objects.get(owner=user)
    return team


def get_season(request: HttpRequest):
    user = request.user
    team = Team.objects.get(owner=user)
    season = Season.objects.filter(team=team).order_by("id").last()
    return season
