import pytest
from django.contrib import auth
from django.shortcuts import reverse
from food.forms import (SignupForm, LoginForm, SearchAdditiveForm,
                        SearchAdditivesForm, SelectLanguageForm,
                        ProductForm)
from food.models import Toxicant


def test_homepage_user_not_logged_in(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.templates[0].name == "homepage.html"


@pytest.mark.django_db
def test_homepage_user_logged_in(client, user):
    response = client.get("/")
    assert response.status_code == 302
    assert response.url == reverse("food:dashboard")


def test_signup_user_not_logged_in(client):
    response = client.get("/signup/")
    assert response.status_code == 200
    assert response.templates[0].name == "signup.html"
    assert isinstance(response.context["form"], SignupForm)


@pytest.mark.django_db
def test_signup_user_logged_in(client, user):
    response = client.get("/signup/")
    assert response.status_code == 302
    assert response.url == reverse("food:dashboard")


def test_login_user_not_logged_in(client):
    response = client.get("/login/")
    assert response.status_code == 200
    assert response.templates[0].name == "login.html"
    assert isinstance(response.context["form"], LoginForm)


@pytest.mark.django_db
def test_login_user_logged_in(client, user):
    response = client.get("/login/")
    assert response.status_code == 302
    assert response.url == reverse("food:dashboard")


def test_logout_user_not_logged_in(client):
    response = client.get("/logout/")
    assert response.status_code == 302
    assert response.url.startswith(reverse("food:login"))


@pytest.mark.django_db
def test_logout_user_logged_in(client, user):
    response = client.get("/logout/")
    assert response.status_code == 302
    assert response.url == reverse("food:homepage")
    user = auth.get_user(client)
    assert user.is_authenticated is False


def test_dashboard_user_not_logged_in(client):
    response = client.get("/dashboard/")
    assert response.status_code == 302
    assert response.url.startswith(reverse("food:login"))


@pytest.mark.django_db
def test_dashboard_user_logged_in(client, user):
    response = client.get("/dashboard/")
    assert response.status_code == 200
    assert response.templates[0].name == "dashboard.html"


def test_search_additive_user_not_logged_in(client):
    response = client.get("/search-additive/")
    assert response.status_code == 302
    assert response.url.startswith(reverse("food:login"))


@pytest.mark.django_db
def test_search_additive_user_logged_in(client, user):
    response = client.get("/search-additive/")
    assert response.status_code == 200
    assert response.templates[0].name == "search_additive.html"
    assert isinstance(response.context["form"], SearchAdditiveForm)


def test_search_additives_user_not_logged_in(client):
    response = client.get("/search-additives/")
    assert response.status_code == 302
    assert response.url.startswith(reverse("food:login"))


@pytest.mark.django_db
def test_search_additives_user_logged_in(client, user):
    response = client.get("/search-additives/")
    assert response.status_code == 200
    assert response.templates[0].name == "search_additives.html"
    assert isinstance(response.context["form"], SearchAdditivesForm)


def test_additive_details_user_not_logged_in(client):
    response = client.get("/additive-details/1/")
    assert response.status_code == 302
    assert response.url.startswith(reverse("food:login"))


@pytest.mark.django_db
def test_additive_details_user_logged_in(client, user, toxicant):
    response = client.get("/additive-details/1/")
    assert response.status_code == 200
    assert response.templates[0].name == "additive_details.html"
    assert response.context["result"] == toxicant


def test_search_additives_by_photo_user_not_logged_in(client):
    response = client.get("/search-additives-by-photo/")
    assert response.status_code == 302
    assert response.url.startswith(reverse("food:login"))


@pytest.mark.django_db
def test_search_additives_by_photo_user_logged_in(client, user):
    response = client.get("/search-additives-by-photo/")
    assert response.status_code == 200
    assert response.templates[0].name == "search_additives_by_photo_1.html"
    assert isinstance(response.context["form"], SelectLanguageForm)


def test_add_harmful_product_user_not_logged_in(client):
    response = client.get("/add-harmful-product/1/")
    assert response.status_code == 302
    assert response.url.startswith(reverse("food:login"))


@pytest.mark.django_db
def test_add_harmful_product_user_logged_in(client, user):
    response = client.get("/add-harmful-product/1/")
    assert response.status_code == 403


@pytest.mark.django_db
def test_add_harmful_product_with_one_toxicant_privileged_user_logged_in(
        client, privileged_user, toxicant):
    print(toxicant.id)
    response = client.get(f"/add-harmful-product/{toxicant.id}/")
    assert response.status_code == 200
    assert response.templates[0].name == "add_product.html"
    assert isinstance(response.context["form"], ProductForm)
    assert response.context["form"].fields["toxicants"].queryset.count() == 1


@pytest.mark.django_db
def test_add_harmful_product_with_two_toxicants_privileged_user_logged_in(
        client, privileged_user, toxicant, toxicant_2):
    response = client.get(f"/add-harmful-product/{toxicant.id},{toxicant_2.id}/")
    assert response.status_code == 200
    assert response.templates[0].name == "add_product.html"
    assert isinstance(response.context["form"], ProductForm)
    assert response.context["form"].fields["toxicants"].queryset.count() == 2


def test_show_harmful_product_user_not_logged_in(client):
    response = client.get("/show-harmful-products/")
    assert response.status_code == 302
    assert response.url.startswith(reverse("food:login"))


@pytest.mark.django_db
def test_show_harmful_product_user_logged_in(client, user):
    response = client.get("/show-harmful-products/")
    assert response.status_code == 403


@pytest.mark.django_db
def test_show_harmful_product_privileged_user_logged_in(
        client, privileged_user, product):
    response = client.get("/show-harmful-products/")
    assert response.status_code == 200
    assert response.templates[0].name == "show_harmful_products.html"
    assert len(response.context["products"]) == 1
