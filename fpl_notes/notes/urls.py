from django.urls import path

from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("season/", views.add_season, name="add_season"),
    path("team/", views.create_team, name="create_team"),
    path("add_player/", views.add_players, name="add_player"),
    path("notes/<slug:slug>/", views.notes_by_tour, name="notes_by_tour"),
    path("notes/<slug:slug>/accept", views.accept_subbstatution, name="accept_sub"),
    path("notes/<slug:slug>/update", views.note_update, name="note_update"),
    path("notes_list/", views.get_notes, name="notes_list"),
    path(
        "notes_list/<str:season>/",
        views.get_notes_list_by_season,
        name="notes_season_list",
    ),
    path("add_notes/", views.add_notes, name="notes"),
]
