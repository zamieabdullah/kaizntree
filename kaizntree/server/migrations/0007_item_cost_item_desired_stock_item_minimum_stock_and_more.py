# Generated by Django 5.0.4 on 2024-04-26 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("server", "0006_category_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="cost",
            field=models.DecimalField(decimal_places=3, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name="item",
            name="desired_stock",
            field=models.DecimalField(decimal_places=3, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name="item",
            name="minimum_stock",
            field=models.DecimalField(decimal_places=3, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name="item",
            name="units",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
