# Generated by Django 3.2.15 on 2022-10-22 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20221022_0243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='center',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
