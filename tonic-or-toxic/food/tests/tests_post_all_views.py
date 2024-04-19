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
    user = User.objects.create_user(username="Jakub", password="Programming01!")
    form_data = {"username": "Jakub", "password": "Programming"}
    response = client.post("/login/", form_data)
    messages = list(get_messages(response.wsgi_request))
    assert "_auth_user_id" not in client.session
    assert response.status_code == 200
    assert len(messages) == 1
    assert str(messages[0]) == "Invalid username or password!"



