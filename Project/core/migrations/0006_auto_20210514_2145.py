# Generated by Django 3.2 on 2021-05-14 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_comics_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='commentforcomics',
            name='date',
            field=models.DateField(auto_now_add=True, verbose_name='Дата создания'),
        ),
    ]