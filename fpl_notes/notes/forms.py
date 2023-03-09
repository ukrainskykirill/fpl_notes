from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import formset_factory

from .models import Note, Player, Season, Team


class AddTeam(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["team_name"]


class AddSeason(forms.ModelForm):
    class Meta:
        model = Season
        fields = ["season_start", "season_end"]


class AddPlayers(forms.ModelForm):
    class Meta:
        model = Player
        fields = ["player", "position", "season"]


class AddNotes(forms.ModelForm):
    class Meta:
        model = Note
        fields = [
            "tour",
            "note",
            "substatution_off",
            "substatution_on",
            "screenshot",
            "slug",
        ]


class AcceptSubstatution(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["substatution_off", "substatution_on"]


AddPlayersFormSet = formset_factory(AddPlayers, extra=15)
