from django.db import models
from tipofii.models import Tipofii
from django.db.models.functions import Upper


class Fii(models.Model):
    codFii = models.CharField(max_length=6, primary_key=True, verbose_name='Codigo', default='', null=False, blank=False)
    nomFii = models.CharField(max_length=50, verbose_name='Nome do fundo imobiliario', default='', null=False, blank=False)
    qtdCotas = models.IntegerField(verbose_name='Quantidade de cotas', null=True)
    valTotal = models.DecimalField(max_digits=15, decimal_places=4, verbose_name='Total investido', null=True)
    datCom = models.CharField(max_length=2,verbose_name='Data Com', null=False, blank=False)
    datPag = models.CharField(max_length=2, verbose_name='Data de pagamento', null=False, blank=False)
    tipFii = models.ForeignKey(Tipofii, null=False, on_delete=models.DO_NOTHING)
    codCor = models.CharField(max_length=7, default='', null=True, blank=True)
    
    def __str__(self):
        return self.codFii
    
    class Meta:
        db_table = 'fii'
        db_table_comment = 'Fundos imobiliarios'
        
    def save(self, *args, **kwargs):
        self.codFii = self.codFii.upper()
        self.nomFii = self.nomFii.upper()
        super(Fii, self).save(*args, **kwargs)
