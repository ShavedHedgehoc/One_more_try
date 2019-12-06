# Generated by Django 2.2.7 on 2019-12-05 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20191125_1824'),
    ]

    operations = [
        migrations.CreateModel(
            name='Declared_Batches',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('decl_quant', models.DecimalField(decimal_places=3, max_digits=7)),
                ('batch_pr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Batch_pr')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Material')),
            ],
        ),
    ]