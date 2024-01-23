# Generated by Django 5.0.1 on 2024-01-23 20:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('fii', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dividendo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qtdCotas', models.IntegerField(verbose_name='Quantidade de cotas')),
                ('valUnitario', models.DecimalField(decimal_places=4, max_digits=15, verbose_name='Valor unitario do dividendo')),
                ('codFii', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='fii.fii', verbose_name='Codigo do fundo imobiliario')),
            ],
            options={
                'db_table': 'dividendo',
                'db_table_comment': 'Dividendos recebidos',
            },
        ),
    ]
