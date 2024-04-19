import pytest
from django.test import Client
from food.models import Toxicant, ToxicantEN, ToxicantPL
from food.views import check_food_additives

client = Client()
@pytest.mark.django_db
def test_function_response():
    response = client.post("/search-additive", {"language": "en", "food_additives": "venom"})
    assert response.status_code == 200

@pytest.mark.django_db
def test_food_additives_search_en(toxicant):
    response = client.post("/search-additive", {"language": "en", "food_additives": "venom"})
    assert response.status_code == 200
    assert "results" in response.context
    assert len(response.context["results"]) == 1


