# Generated by Django 2.2 on 2020-11-17 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20201012_2141'),
    ]

    operations = [
        migrations.AddField(
            model_name='main',
            name='seo_keywords',
            field=models.TextField(default='-'),
        ),
        migrations.AddField(
            model_name='main',
            name='seo_txt',
            field=models.CharField(default='-', max_length=160),
        ),
    ]
