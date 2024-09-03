# Generated by Django 1.10.6 on 2017-03-30 08:54
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("lava_scheduler_app", "0025_switch_job_status_trigger_type")]

    operations = [
        migrations.AddField(
            model_name="devicetype",
            name="disable_health_check",
            field=models.BooleanField(
                default=False,
                verbose_name="Disable health check for devices of this type",
            ),
        )
    ]
