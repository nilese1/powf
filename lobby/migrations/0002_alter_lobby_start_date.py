# Generated by Django 5.1.4 on 2025-01-06 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lobby", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lobby",
            name="start_date",
            field=models.DateTimeField(verbose_name="date started"),
        ),
    ]
