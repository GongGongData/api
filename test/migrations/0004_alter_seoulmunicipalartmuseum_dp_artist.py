# Generated by Django 4.2.11 on 2024-04-13 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("test", "0003_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="seoulmunicipalartmuseum",
            name="DP_ARTIST",
            field=models.CharField(max_length=1000),
        ),
    ]