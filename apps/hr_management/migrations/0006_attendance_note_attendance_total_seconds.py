# Generated by Django 4.1.5 on 2023-01-21 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hr_management", "0005_alter_attendance_time_in_alter_attendance_time_out"),
    ]

    operations = [
        migrations.AddField(
            model_name="attendance",
            name="note",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="attendance",
            name="total_seconds",
            field=models.IntegerField(blank=True, editable=False, null=True),
        ),
    ]