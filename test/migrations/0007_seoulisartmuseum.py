# Generated by Django 4.2.11 on 2024-04-14 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("test", "0006_alter_seoulmunicipalartmuseum_dp_art_cnt_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="SeoulisArtMuseum",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("GA_KNAME", models.CharField(max_length=255)),
                ("GA_INS_DATE", models.DateField()),
                ("CODE_N1_NAME", models.CharField(max_length=1000)),
                ("CODE_N2_NAME", models.CharField(max_length=1000)),
                ("CODE_N3_NAME", models.CharField(max_length=1000)),
                ("GA_ADDR1", models.CharField(max_length=1000)),
                ("GA_ADDR2", models.CharField(blank=True, max_length=1000)),
                ("GA_DETAIL", models.TextField()),
                ("CODE_A1", models.CharField(blank=True, max_length=1000)),
            ],
        ),
    ]