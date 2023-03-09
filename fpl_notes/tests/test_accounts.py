import pytest
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.django_db
def test_user_create():
    User.objects.create_user("john", "lennon@thebeatles.com", "johnpassword")
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_register(client):
    url = reverse("register")
    data = {
        "username": "kir24_uk",
        "email": "kir@kir.com",
        "password1": "abcd5678",
        "password2": "abcd5678",
    }
    response = client.post(url, data, follow=True)
    assert response.status_code == 200
    username_on_home_page = b"kir24_uk"
    assert username_on_home_page in response.content
    assert User.objects.count() == 1


def test_home_page_public_access(client):
    url = reverse("home")
    response = client.get(url)
    assert response.status_code == 200


@pytest.fixture
def myuser(django_user_model):
    user = django_user_model.objects.create_user(
        username="kiruk24", password="abcd5678"
    )
    return user


def test_logged_in_client(client, myuser):
    url = reverse("create_team")
    client.login(username="kiruk24", password="abcd5678")
    response = client.get(url)
    assert response.status_code == 200
    client.logout()
    response = client.get(url)
    assert response.status_code == 302


def test_private_access_redirect_to_login(client):
    url = reverse("create_team")
    response = client.get(url, follow=True)
    assert 1 == len(response.redirect_chain)
    assert response.status_code == 200
