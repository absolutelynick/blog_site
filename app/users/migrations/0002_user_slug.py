# Generated by Django 2.2 on 2020-01-06 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("users", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="user",
            name="slug",
            field=models.SlugField(max_length=64, null=True, unique=True),
        )
    ]