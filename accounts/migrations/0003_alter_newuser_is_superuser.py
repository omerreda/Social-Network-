# Generated by Django 4.1.3 on 2022-11-23 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_newuser_groups_newuser_is_superuser_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newuser',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]