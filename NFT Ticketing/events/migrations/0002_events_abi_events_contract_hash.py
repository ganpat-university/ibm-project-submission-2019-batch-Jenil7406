# Generated by Django 4.1.7 on 2023-04-04 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="events",
            name="abi",
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="events",
            name="contract_hash",
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]
