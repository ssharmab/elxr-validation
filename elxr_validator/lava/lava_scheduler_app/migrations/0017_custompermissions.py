# Generated by Django 1.9.6 on 2016-05-26 07:58
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("lava_scheduler_app", "0016_index_testjob_submit_time")]

    operations = [
        migrations.AlterModelOptions(
            name="testjobuser",
            options={
                "permissions": (
                    ("cancel_resubmit_testjob", "Can cancel or resubmit test jobs"),
                )
            },
        )
    ]