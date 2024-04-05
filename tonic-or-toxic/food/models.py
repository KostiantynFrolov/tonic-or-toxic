from django.db import models


class ToxicantEN(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    medical_risks = models.CharField(max_length=100, null=True)
    names = models.CharField(max_length=100, null=True, unique=True)


class ToxicantPL(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    medical_risks = models.CharField(max_length=100, null=True)
    names = models.CharField(max_length=100, null=True, unique=True)


ToxicantScale = (
    (1, 'least harmful'),
    (2, 'moderately harmful'),
    (3, 'harmful'),
    (4, 'very harmful')
)


class Toxicant(models.Model):
    toxicant_en = models.OneToOneField(ToxicantEN, on_delete=models.CASCADE, blank=True)
    toxicant_pl = models.OneToOneField(ToxicantPL, on_delete=models.CASCADE, blank=True)
    scale = models.IntegerField(choices=ToxicantScale)


class Product(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100, blank=True)
    toxicants = models.ManyToManyField(Toxicant)
    adding_date = models.DateField(auto_now_add=True)

