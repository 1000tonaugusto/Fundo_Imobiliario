from django.db import models
from tipofii.models import Tipofii


class Fii(models.Model):
    codFii = models.CharField(max_length=6, primary_key=True, verbose_name='Codigo do fundo imobiliario', default='')
    nomFii = models.CharField(max_length=50, verbose_name='Nome do fundo imobiliario', default='')
    qtdCotas = models.IntegerField(verbose_name='Quantidade de cotas')
    valTotal = models.DecimalField(max_digits=15, decimal_places=4, verbose_name='Total investido')
    datCom = models.DateField(verbose_name='Data Com')
    datPag = models.DateField(verbose_name='Data de pagamento')
    tipoFii = models.ForeignKey(Tipofii, null=False, on_delete=models.DO_NOTHING)
    
    class Meta:
        db_table = 'fii'
        db_table_comment = 'Fundos imobiliarios'
