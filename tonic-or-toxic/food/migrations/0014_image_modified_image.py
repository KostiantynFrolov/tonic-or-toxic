# Generated by Django 4.2 on 2024-04-11 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0013_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='modified_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]