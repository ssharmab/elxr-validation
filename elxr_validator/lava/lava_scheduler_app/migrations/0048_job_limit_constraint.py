# Generated by Django 2.2.9 on 2020-01-28 10:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("lava_scheduler_app", "0047_job_limit")]

    operations = [
        migrations.AlterField(
            model_name="worker",
            name="job_limit",
            field=models.PositiveIntegerField(default=0),
        )
    ]