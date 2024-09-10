# Generated by Django 1.11.28 on 2020-03-23 15:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0008_alter_user_username_max_length"),
        ("lava_scheduler_app", "0048_job_limit_constraint"),
    ]

    operations = [
        migrations.CreateModel(
            name="GroupWorkerPermission",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="auth.Group"
                    ),
                ),
                (
                    "permission",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="auth.Permission",
                    ),
                ),
                (
                    "worker",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="permissions",
                        to="lava_scheduler_app.Worker",
                    ),
                ),
            ],
        ),
        migrations.AlterUniqueTogether(
            name="groupworkerpermission",
            unique_together={("group", "permission", "worker")},
        ),
    ]