# Generated by Django 4.1.7 on 2023-04-11 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0003_alter_events_abi_alter_events_contract_hash"),
    ]

    operations = [
        migrations.AddField(
            model_name="events",
            name="contract_address",
            field=models.TextField(default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="events",
            name="abi",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="events",
            name="contract_hash",
            field=models.TextField(),
        ),
    ]
