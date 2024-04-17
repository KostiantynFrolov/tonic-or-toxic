import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from food.models import ToxicantEN, ToxicantPL, Toxicant, Product, Image


@pytest.fixture
def toxicant_en():
    test_toxicant_en = ToxicantEN.objects.create(
        name="dangerous toxicant", description="It's everywhere",
        medical_risks="cancer", names="poison venom")
    return test_toxicant_en

@pytest.fixture
def toxicant_pl():
    test_toxicant_pl = ToxicantPL.objects.create(
        name="niebezpieczna substancja", description="To jest wszędzie",
        medical_risks="nowotwór", names="trucizna jad")
    return test_toxicant_pl

@pytest.fixture
def toxicant(toxicant_en, toxicant_pl):
    test_toxicant = Toxicant.objects.create(
        toxicant_en=toxicant_en, toxicant_pl=toxicant_pl, scale="vh")
    return test_toxicant

@pytest.fixture()
def product(toxicant):
    test_product = Product.objects.create(
        name="ham", manufacturer="Ham master")
    test_product.toxicants.add(toxicant)
    return test_product

@pytest.fixture()
def image():
    image_content = b"simple_image_file_content"
    image_file = SimpleUploadedFile(
        "image.jpg", content=image_content, content_type="image/jpeg")
    test_image = Image.objects.create(image=image_file)
    return test_image



