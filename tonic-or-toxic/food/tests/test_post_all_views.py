import pytest
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.shortcuts import reverse


@pytest.mark.django_db
def test_signup_user_not_logged_in(client):
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
def test_login_correct_user_not_logged_in(client):
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
def test_login_incorrect_user_not_logged_in(client):
    User.objects.create_user(username="Jakub", password="Programming01!")
    form_data = {"username": "Jakub", "password": "Programming"}
    response = client.post("/login/", form_data)
    messages = list(get_messages(response.wsgi_request))
    assert "_auth_user_id" not in client.session
    assert response.status_code == 200
    assert len(messages) == 1
    assert str(messages[0]) == "Invalid username or password!"


@pytest.mark.django_db
def test_search_additive_user_logged_in_en_name_in_database(client, user, toxicant):
    form_data = {"language": "en", "additive_name": "veno"}
    response = client.post("/search-additive/", form_data)
    assert response.status_code == 200
    assert len(response.context["results"]) == 1
    assert toxicant in response.context["results"]
    assert int(response.context["results_id"].split(",")[0]) == toxicant.id


@pytest.mark.django_db
def test_search_additive_user_logged_in_pl_name_in_database(client, user, toxicant):
    form_data = {"language": "pl", "additive_name": "jad"}
    response = client.post("/search-additive/", form_data)
    assert response.status_code == 200
    assert len(response.context["results"]) == 1
    assert toxicant in response.context["results"]
    assert int(response.context["results_id"].split(",")[0]) == toxicant.id


@pytest.mark.django_db
def test_search_additive_user_logged_in_en_no_name_in_database(
        client, user, toxicant):
    form_data = {"language": "en", "additive_name": "trans fat"}
    response = client.post("/search-additive/", form_data)
    assert response.status_code == 200
    assert len(response.context["results"]) == 0
    assert response.context["results_id"] == ""


@pytest.mark.django_db
def test_search_additive_user_logged_in_pl_no_name_in_database(
        client, user, toxicant):
    form_data = {"language": "pl", "additive_name": "azorubina"}
    response = client.post("/search-additive/", form_data)
    assert response.status_code == 200
    assert len(response.context["results"]) == 0
    assert response.context["results_id"] == ""


@pytest.mark.django_db
def test_search_additives_user_logged_in_en_names_in_database(
        client, user, toxicant, toxicant_2):
    form_data = {"language": "en", "additive_names": "poison , aloe vera"}
    response = client.post("/search-additives/", form_data)
    assert response.status_code == 200
    assert len(response.context["results"]) == 2
    assert str(toxicant.id) in response.context["results_id"].split(",")
    assert str(toxicant_2.id) in response.context["results_id"].split(",")
    assert toxicant in response.context["results"]
    assert toxicant_2 in response.context["results"]


@pytest.mark.django_db
def test_search_additives_user_logged_in_pl_names_in_database(
        client, user, toxicant, toxicant_2):
    form_data = {"language": "pl", "additive_names": "truciz,aloes właś"}
    response = client.post("/search-additives/", form_data)
    assert response.status_code == 200
    assert len(response.context["results"]) == 2
    assert str(toxicant.id) in response.context["results_id"].split(",")
    assert str(toxicant_2.id) in response.context["results_id"].split(",")
    assert toxicant in response.context["results"]
    assert toxicant_2 in response.context["results"]


@pytest.mark.django_db
def test_search_additives_user_logged_in_en_name_in_database(
        client, user, toxicant, toxicant_2):
    form_data = {"language": "en", "additive_names": "poison , aspartame "}
    response = client.post("/search-additives/", form_data)
    assert response.status_code == 200
    assert len(response.context["results"]) == 1
    assert str(toxicant.id) in response.context["results_id"].split(",")
    assert toxicant in response.context["results"]


@pytest.mark.django_db
def test_search_additives_user_logged_in_pl_name_in_database(
        client, user, toxicant, toxicant_2):
    form_data = {"language": "pl", "additive_names": "trucizna , aspartam "}
    response = client.post("/search-additives/", form_data)
    assert response.status_code == 200
    assert len(response.context["results"]) == 1
    assert str(toxicant.id) in response.context["results_id"].split(",")
    assert toxicant in response.context["results"]


@pytest.mark.django_db
def test_search_additives_user_logged_in_en_no_name_in_database(
        client, user, toxicant, toxicant_2):
    form_data = {"language": "en", "additive_names": " cyclamate , aspartame "}
    response = client.post("/search-additives/", form_data)
    assert response.status_code == 200
    assert len(response.context["results"]) == 0
    assert response.context["results_id"] == ""


@pytest.mark.django_db
def test_search_additives_user_logged_in_pl_no_name_in_database(
        client, user, toxicant, toxicant_2):
    form_data = {"language": "pl", "additive_names": " cyclamat , aspartam"}
    response = client.post("/search-additives/", form_data)
    assert response.status_code == 200
    assert len(response.context["results"]) == 0
    assert response.context["results_id"] == ""


@pytest.mark.django_db
def test_add_harmful_product_with_one_toxicant_privileged_user_logged_in(
        client, privileged_user, toxicant):
    form_data = {
        "name": "Harmful product",
        "manufacturer": "Bad manufacturer",
        "toxicants": [toxicant.id],
    }
    response = client.post(f"/add-harmful-product/{toxicant.id}/", form_data)
    assert response.status_code == 302
    assert response.url == reverse("food:show_harmful_products")
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert str(messages[0]) == ("Congratulations! You have successfully"
                                " added the harmful product.")


@pytest.mark.django_db
def test_add_harmful_product_with_two_toxicants_privileged_user_logged_in(
        client, privileged_user, toxicant, toxicant_2):
    form_data = {
        "name": "Harmful product",
        "manufacturer": "Bad manufacturer",
        "toxicants": [toxicant.id, toxicant_2.id],
    }
    response = client.post(
        f"/add-harmful-product/{toxicant.id},{toxicant_2.id}/", form_data)
    assert response.status_code == 302
    assert response.url == reverse("food:show_harmful_products")
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert str(messages[0]) == ("Congratulations! You have successfully"
                                " added the harmful product.")
