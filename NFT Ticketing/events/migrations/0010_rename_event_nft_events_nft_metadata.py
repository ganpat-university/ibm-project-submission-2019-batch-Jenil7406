# Generated by Django 4.1.7 on 2023-04-19 19:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0009_events_event_nft"),
    ]

    operations = [
        migrations.RenameField(
            model_name="events",
            old_name="event_nft",
            new_name="nft_metadata",
        ),
    ]
