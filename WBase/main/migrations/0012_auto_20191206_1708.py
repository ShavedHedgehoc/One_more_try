# Generated by Django 2.2.7 on 2019-12-06 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_declared_batches'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lot',
            options={'ordering': ['lot_code']},
        ),
    ]
