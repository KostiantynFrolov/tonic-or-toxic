import pytest
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.shortcuts import reverse


@pytest.mark.django_db
def test_signup(client):
    form_data = {
        "username": "Jakub",
        "email": "jakub@gmail.com",
        "password1": "Programming01!",
        "password2": "Programming01!"
    }
    response = client.post("/signup/", form_data)
    assert User.objects.filter(username="Jakub").exists()
    assert response.status_code == 302
    assert response.url == reverse("food:login")
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert str(messages[0]) == ("Congratulations! Your signup is complete. "
                                "You can now log in.")


@pytest.mark.django_db
def test_login_correct(client):
    user = User.objects.create_user(username="Jakub", password="Programming01!")
    form_data = {"username": "Jakub", "password": "Programming01!"}
    response = client.post("/login/", form_data)
    messages = list(get_messages(response.wsgi_request))
    assert user.id == int(client.session["_auth_user_id"])
    assert response.status_code == 302
    assert response.url == reverse("food:dashboard")
    assert len(messages) == 1
    assert str(messages[0]) == "Congratulations! You have successfully logged in."


@pytest.mark.django_db
def test_login_incorrect(client):
    User.objects.create_user(username="Jakub", password="Programming01!")
    form_data = {"username": "Jakub", "password": "Programming"}
    response = client.post("/login/", form_data)
    messages = list(get_messages(response.wsgi_request))
    assert "_auth_user_id" not in client.session
    assert response.status_code == 200
    assert len(messages) == 1
    assert str(messages[0]) == "Invalid username or password!"


@pytest.mark.django_db
def test_search_additive_en_correct(client, user, toxicant):
    form_data = {"language": "en", "additive_name": "veno"}
    response = client.post("/search-additive/", form_data)
    assert response.status_code == 200
    assert len(response.context["results"]) == 1
    assert list(response.context["results"])[0].id == toxicant.id
    assert int(response.context["results_id"].split(",")[0]) == toxicant.id


@pytest.mark.django_db
def test_search_additive_pl_correct(client, user, toxicant):
    form_data = {"language": "pl", "additive_name": "jad"}
    response = client.post("/search-additive/", form_data)
    assert response.status_code == 200
    assert len(response.context["results"]) == 1
    assert list(response.context["results"])[0].id == toxicant.id
    assert int(response.context["results_id"].split(",")[0]) == toxicant.id


@pytest.mark.django_db
def test_search_additive_en_no_name_in_database(client, user, toxicant):
    form_data = {"language": "en", "additive_name": "trans fat"}
    response = client.post("/search-additive/", form_data)
    assert response.status_code == 200
    assert len(response.context["results"]) == 0


@pytest.mark.django_db
def test_search_additive_pl_no_name_in_database(client, user, toxicant):
    form_data = {"language": "pl", "additive_name": "azorubina"}
    response = client.post("/search-additive/", form_data)
    assert response.status_code == 200
    assert len(response.context["results"]) == 0

