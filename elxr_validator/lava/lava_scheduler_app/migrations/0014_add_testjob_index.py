# Generated by Django 1.9.5 on 2016-04-27 08:50
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("lava_scheduler_app", "0013_auto_20160302_0404")]

    operations = [
        migrations.AlterIndexTogether(
            name="testjob",
            index_together={("status", "requested_device_type", "requested_device")},
        )
    ]