# Generated by Django 4.2 on 2024-04-02 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0006_alter_toxicant_scale_alter_toxicanten_names'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toxicanten',
            name='names',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]
