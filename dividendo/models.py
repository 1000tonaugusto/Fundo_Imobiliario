from django.db import models
from fii.models import Fii
from decimal import Decimal
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from fii.models import Fii


class Dividendo(models.Model):
    datPaga = models.DateField(verbose_name='Data do movimento', blank=True, null=True)
    qtdCotas = models.IntegerField(verbose_name='Quantidade de cotas')
    valUnitario = models.DecimalField(max_digits=15, decimal_places=4, verbose_name='Valor unitario do dividendo')
    codFii = models.ForeignKey(Fii, null=False, on_delete=models.DO_NOTHING, verbose_name='Codigo do fundo imobiliario')
    valTotal = models.DecimalField(max_digits=15, decimal_places=4, verbose_name='Valor Total')
    
    class Meta:
        db_table = 'dividendo'
        db_table_comment = 'Dividendos recebidos'
        
    def __str__(self):
        return self.codFii_id
    
    @property
    def get_values(self):
        valor_total = Decimal(self.valUnitario)*Decimal(self.qtdCotas)
        return valor_total
    
    def save(self, *args, **kwargs):
        self.valTotal = self.get_values
        super(Dividendo, self).save(*args, **kwargs)


@receiver(post_save, sender=Dividendo)
def atualiza_fii(sender, instance, **kwargs):
    codFii_id = instance.codFii
    fii = Fii.objects.filter(codFii=codFii_id).first()
    if fii:
        fii.valDividendo = fii.valDividendo + instance.valTotal
        fii.save()
        
@receiver(post_delete, sender=Dividendo)
def atualiza_fii_del(sender, instance, **kwargs):
    codFii_id = instance.codFii
    fii = Fii.objects.filter(codFii=codFii_id).first()
    if fii:
        fii.valDividendo = fii.valDividendo - instance.valTotal
        fii.save()