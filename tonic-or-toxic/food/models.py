from django.db import models


class ToxicantEN(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    medical_risks = models.CharField(max_length=100, blank=True)
    names = models.CharField(max_length=100, unique=True)


class ToxicantPL(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    medical_risks = models.CharField(max_length=100, blank=True)
    names = models.CharField(max_length=100, unique=True)


class Toxicant(models.Model):
    LOW = 'l'
    MODERATE = 'm'
    HIGH = 'h'
    VERY_HIGH = 'vh'
    TOXICANTS_SCALE = (
        (LOW, 'low'),
        (MODERATE, 'moderate'),
        (HIGH, 'high'),
        (VERY_HIGH, 'very high')
    )
    toxicant_en = models.OneToOneField(
        ToxicantEN, on_delete=models.CASCADE, null=True)
    toxicant_pl = models.OneToOneField(
        ToxicantPL, on_delete=models.CASCADE, null=True)
    scale = models.CharField(max_length=10, choices=TOXICANTS_SCALE)


class Product(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100, blank=True)
    toxicants = models.ManyToManyField(Toxicant)
    adding_date = models.DateField(auto_now_add=True)


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
