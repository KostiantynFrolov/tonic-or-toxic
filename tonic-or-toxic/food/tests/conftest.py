import pytest
from django.contrib.auth.models import Permission, User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from food.models import Image, Product, Toxicant, ToxicantEN, ToxicantPL


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


@pytest.fixture
def product(toxicant):
    test_product = Product.objects.create(
        name="ham", manufacturer="Ham master")
    test_product.toxicants.add(toxicant)
    return test_product


@pytest.fixture
def image():
    image_content = b"simple_image_file_content"
    image_file = SimpleUploadedFile(
        "image.jpg", content=image_content, content_type="image/jpeg")
    test_image = Image.objects.create(image=image_file)
    return test_image


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def user(client):
    user = User.objects.create_user(
        username="user", email="user@gmail.com", password="UserPassword01!")
    client.force_login(user)
    return user


@pytest.fixture
def privileged_user(client):
    permission = Permission.objects.get(codename="add_product")
    privileged_user = User.objects.create_user(
        username="privileged_user",
        email="privileged@gmail.com",
        password="PrivilegedPassword01!")
    privileged_user.user_permissions.add(permission)
    client.force_login(privileged_user)
    return privileged_user
