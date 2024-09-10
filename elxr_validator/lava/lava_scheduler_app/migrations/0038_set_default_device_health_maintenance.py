# Generated by Django 1.11.14 on 2018-07-17 09:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("lava_scheduler_app", "0037_notify_callback_separation")]

    operations = [
        migrations.AlterField(
            model_name="device",
            name="health",
            field=models.IntegerField(
                choices=[
                    (0, "Good"),
                    (1, "Unknown"),
                    (2, "Looping"),
                    (3, "Bad"),
                    (4, "Maintenance"),
                    (5, "Retired"),
                ],
                default=4,
            ),
        )
    ]