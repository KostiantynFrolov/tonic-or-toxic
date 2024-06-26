# Generated by Django 4.2 on 2024-03-31 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0004_alter_toxicanten_name_alter_toxicantpl_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='toxicanten',
            name='names',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='toxicantpl',
            name='names',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='toxicanten',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='toxicantpl',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
