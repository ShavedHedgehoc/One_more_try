# Generated by Django 2.2.7 on 2019-11-20 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='material_name',
            field=models.CharField(max_length=200),
        ),
    ]
