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
    toxicant_en = models.OneToOneField(ToxicantEN, on_delete=models.CASCADE, null=True)
    toxicant_pl = models.OneToOneField(ToxicantPL, on_delete=models.CASCADE, null=True)
    scale = models.CharField(max_length=10, choices=(
        ('low', 'low'),
        ('moderate', 'moderate'),
        ('high', 'high'),
        ('very high', 'very high')
    ))


class Product(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100, blank=True)
    toxicants = models.ManyToManyField(Toxicant)
    adding_date = models.DateField(auto_now_add=True)

