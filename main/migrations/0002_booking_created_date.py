# Generated by Django 4.1.3 on 2022-12-26 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='created_date',
            field=models.DateField(auto_now=True),
        ),
    ]