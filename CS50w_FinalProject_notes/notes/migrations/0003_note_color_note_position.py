# Generated by Django 4.2.7 on 2023-11-23 19:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("notes", "0002_note"),
    ]

    operations = [
        migrations.AddField(
            model_name="note",
            name="color",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="note",
            name="position",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
