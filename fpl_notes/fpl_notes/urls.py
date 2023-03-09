from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("fpl_notes/", include("notes.urls"), name="fpl_notes"),
    path("accounts/", include("accounts.urls"), name="accounts_urls"),
]
