# Generated by Django 4.2 on 2024-03-27 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0002_alter_toxicanten_name_alter_toxicantpl_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='toxicanten',
            name='medical_risks',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='toxicantpl',
            name='medical_risks',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='toxicanten',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='toxicantpl',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
