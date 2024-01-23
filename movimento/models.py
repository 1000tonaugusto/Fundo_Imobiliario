from django.db import models
from fii.models import Fii


class Movimento(models.Model):
    MOVIMENTO_CHOICES = (('C','Compra'), ('V','Venda'))
    datMovimento = models.DateField(verbose_name='Data do movimento')
    qtdCotas  = models.IntegerField(verbose_name='Informe quantidade')
    valUnitario = models.DecimalField(max_digits=15, decimal_places=4, verbose_name='Valor unitário de cota')
    tipMovimento = models.CharField(max_length=1, choices=MOVIMENTO_CHOICES)
    codFii = models.ForeignKey(Fii, null=False, on_delete=models.DO_NOTHING, verbose_name='Codigo do fundo imobiliario')
    
    class Meta:
        db_table = 'movimento'
        db_table_comment = 'Compra e venda de ativos'