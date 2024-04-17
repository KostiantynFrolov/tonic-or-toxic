import os
import pytest
from django.db import IntegrityError
from django.utils import timezone
from food.models import ToxicantEN, ToxicantPL, Toxicant, Product, Image
@pytest.mark.django_db

def test_toxicanten_model(toxicant_en):
    tox_en = ToxicantEN.objects.get(name="dangerous toxicant")
    assert tox_en == toxicant_en
    assert tox_en.description == "It's everywhere"
    assert tox_en.medical_risks == "cancer"
    assert tox_en.names == "poison venom"
    assert len(ToxicantEN.objects.all()) == 1
    with pytest.raises(IntegrityError):
        ToxicantEN.objects.create(
            name="bad toxicant", description="Created by humans",
            medical_risks="DNA damage", names="poison venom")

@pytest.mark.django_db
def test_toxicantpl_model(toxicant_pl):
    tox_pl = ToxicantPL.objects.get(name="niebezpieczna substancja")
    assert tox_pl == toxicant_pl
    assert tox_pl.description == "To jest wszędzie"
    assert tox_pl.medical_risks == "nowotwór"
    assert tox_pl.names == "trucizna jad"
    assert len(ToxicantPL.objects.all()) == 1
    with pytest.raises(IntegrityError):
        ToxicantPL.objects.create(
            name="zły toksynant", description="Stworzony przez ludzi",
            medical_risks="Uszkodzenie DNA", names="trucizna jad")

@pytest.mark.django_db
def test_toxicant(toxicant, toxicant_en, toxicant_pl):
    assert toxicant.scale == "vh"
    assert len(Toxicant.objects.all()) == 1
    assert toxicant.toxicant_en == toxicant_en
    assert toxicant.toxicant_pl == toxicant_pl

@pytest.mark.django_db
def test_product(product, toxicant):
    prod = Product.objects.get(name="ham")
    assert prod == product
    assert prod.name == "ham"
    assert prod.manufacturer == "Ham master"
    assert toxicant in prod.toxicants.all()
    assert len(Product.objects.all()) == 1
    assert prod.adding_date == timezone.now().date()

@pytest.mark.django_db
def test_image(image):
    img = Image.objects.first()
    assert img == image
    assert img.image.file.read() == b"simple_image_file_content"
    assert img.image.url == "/media/images/image.jpg"
    assert len(Image.objects.all()) == 1
    if os.path.isfile(img.image.path):
        os.remove(img.image.path)


