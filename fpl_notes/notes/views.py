from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import AcceptSubstatution, AddNotes, AddPlayersFormSet, AddSeason, AddTeam
from .services.fpl_magic import (
    get_note_by_tour,
    get_season,
    get_seasons_and_notes,
    get_team,
    substatution,
    validation_by_position,
)
from .utils import menu, sub


def home(request: HttpRequest) -> HttpResponse:
    context = {"menu": menu}
    return render(request, template_name="notes/base.html", context=context)


@login_required(redirect_field_name="login")
def add_season(request: HttpRequest) -> HttpResponse:
    form = AddSeason(request.POST)
    if request.method == "POST":
        if form.is_valid():
            season = form.save(commit=False)
            team = get_team(request=request)
            season.team = team
            form.save()
        return redirect("home")
    context = {"form": form, "menu": menu}
    return render(request, template_name="notes/my_team.html", context=context)


@login_required(redirect_field_name="login")
def create_team(request: HttpRequest) -> HttpResponse:
    form = AddTeam(request.POST)
    if request.method == "POST":
        if form.is_valid():
            team_form = form.save(commit=False)
            team_form.owner = request.user
            form.save()
        return redirect("add_season")
    context = {"form": form, "menu": menu}
    return render(request, template_name="notes/my_team.html", context=context)


@login_required(redirect_field_name="login")
def add_players(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        formset = AddPlayersFormSet(request.POST)
        if formset.is_valid() and validation_by_position(request=request):
            for form in formset:
                if form.is_valid():
                    player = form.save(commit=False)
                    team = get_team(request=request)
                    player.team = team
                    form.save()
            return redirect("home")
        else:
            rule = "В команде может быть 2 GK, 5 DR, 5 MD, 3 FW"
            context = {"formset": formset, "menu": menu, "rules": rule}
            return render(request, template_name="notes/add_team.html", context=context)
    formset = AddPlayersFormSet()
    context = {"formset": formset, "menu": menu}
    return render(request, template_name="notes/add_team.html", context=context)


@login_required(redirect_field_name="login")
def add_notes(request: HttpRequest) -> HttpResponse:
    form = AddNotes(request.POST, request.FILES)
    if request.method == "POST":
        if form.is_valid():
            note = form.save(commit=False)
            note.author = get_team(request=request)
            note.season = get_season(request=request)
            form.save()
        context = {"form": form, "menu": menu}
        return render(request, template_name="notes/add_note.html", context=context)
    else:
        context = {"form": form, "menu": menu}
        return render(request, template_name="notes/add_note.html", context=context)


@login_required(redirect_field_name="login")
def notes_by_tour(request: HttpRequest, slug: str) -> HttpResponse:
    note = get_note_by_tour(request=request, slug=slug)
    context = {"menu": menu, "note": note, "sub": sub}
    return render(request, template_name="notes/note.html", context=context)


@login_required(redirect_field_name="login")
def note_update(request: HttpRequest, slug: str) -> HttpResponse:
    note = get_note_by_tour(request=request, slug=slug)
    if request.method == "POST":
        form = AddNotes(request.POST, instance=note)
        if form.is_valid():
            form.save()
        context = {"form": form, "menu": menu}
        return render(request, template_name="notes/update_note.html", context=context)
    form = AddNotes(instance=note)
    context = {"menu": menu, "form": form}
    return render(request, template_name="notes/update_note.html", context=context)


@login_required(redirect_field_name="login")
def accept_subbstatution(request: HttpRequest, slug: str) -> HttpResponse:
    note = get_note_by_tour(request, slug)
    if request.method == "POST":
        form = AcceptSubstatution(request.POST, instance=note)
        if form.is_valid():
            form.save(commit=False)
            substatution(data=request.POST)
            form.save()
        context = {"form": form, "menu": menu}
        return render(request, template_name="notes/add_note.html", context=context)
    form = AcceptSubstatution(instance=note)
    context = {"menu": menu, "form": form}
    return render(request, template_name="notes/accept_sub.html", context=context)


@login_required(redirect_field_name="login")
def get_notes_list(request: HttpRequest) -> HttpResponse:
    notes, seasons = get_seasons_and_notes(request=request)
    context = {"menu": menu, "seasons": seasons, "notes": notes}
    return render(request, template_name="notes/notes_list.html", context=context)


@login_required(redirect_field_name="login")
def get_notes_list_by_season(request: HttpRequest, season: str) -> HttpResponse:
    notes, seasons = get_seasons_and_notes(request=request, season=season)
    context = {"menu": menu, "seasons": seasons, "notes": notes}
    return render(request, template_name="notes/notes_list.html", context=context)


@login_required(redirect_field_name="login")
def get_notes(request: HttpRequest, season: str = None) -> HttpResponse:
    notes, seasons = get_seasons_and_notes(request=request, season=season)
    context = {"menu": menu, "seasons": seasons, "notes": notes}
    return render(request, template_name="notes/notes_list.html", context=context)
