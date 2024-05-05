# Generated by Django 4.2.11 on 2024-05-05 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("test", "0024_searchhistory"),
    ]

    operations = [
        migrations.AlterField(
            model_name="searchhistory",
            name="LANDMARK",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="search_history",
                to="test.landmark",
            ),
        ),
    ]
