# Generated by Django 2.2 on 2020-10-27 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0002_auto_20201027_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='email',
            field=models.TextField(default=''),
        ),
    ]