# Generated by Django 3.2 on 2021-05-14 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20210514_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='publication_date',
            field=models.DateField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='comics',
            name='publication_date',
            field=models.DateField(auto_now_add=True, verbose_name='Дата создания'),
        ),
    ]
