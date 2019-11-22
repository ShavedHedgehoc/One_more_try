# Generated by Django 2.2.7 on 2019-11-22 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20191122_2209'),
    ]

    operations = [
        migrations.AddField(
            model_name='lot',
            name='lot_expire',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lot',
            name='lot_code',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
