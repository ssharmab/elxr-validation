# Generated by Django 1.11.10 on 2018-02-07 09:56
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("lava_scheduler_app", "0034_worker_last_ping")]

    operations = [migrations.RemoveField(model_name="testjob", name="_results_link")]