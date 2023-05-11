# Generated by Django 4.1.5 on 2023-01-21 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("hr_management", "0006_attendance_note_attendance_total_seconds"),
    ]

    operations = [
        migrations.CreateModel(
            name="AttendanceByMonth",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "month",
                    models.IntegerField(
                        choices=[
                            (1, "January"),
                            (2, "February"),
                            (3, "March"),
                            (4, "April"),
                            (5, "May"),
                            (6, "June"),
                            (7, "July"),
                            (8, "August"),
                            (9, "September"),
                            (10, "October"),
                            (11, "November"),
                            (12, "December"),
                        ]
                    ),
                ),
                ("year", models.IntegerField()),
                ("total_work_days", models.IntegerField(default=0)),
                ("total_work_hours", models.FloatField(default=0)),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="hr_management.employee",
                    ),
                ),
            ],
        ),
    ]
