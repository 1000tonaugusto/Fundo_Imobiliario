# Generated by Django 5.0.1 on 2024-02-27 10:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fii', '0006_alter_fii_options'),
        ('movimento', '0002_movimento_valtotal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimento',
            name='codFii',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='fii.fii', verbose_name='Codigo'),
        ),
    ]
