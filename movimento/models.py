from django.db import models
from decimal import Decimal
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from fii.models import Fii


class Movimento(models.Model):
    MOVIMENTO_CHOICES = (('C','Compra'), ('V','Venda'))
    datMovimento = models.DateField(verbose_name='Data do movimento')
    qtdCotas  = models.IntegerField(verbose_name='Informe quantidade')
    valUnitario = models.DecimalField(max_digits=15, decimal_places=4, verbose_name='Valor unitário de cota')
    tipMovimento = models.CharField(max_length=1, choices=MOVIMENTO_CHOICES)
    codFii = models.ForeignKey(Fii, null=False, on_delete=models.DO_NOTHING, verbose_name='Codigo')
    valTotal = models.DecimalField(max_digits=15, decimal_places=4, verbose_name='Valor Total', default=0)
    
    class Meta:
        db_table = 'movimento'
        db_table_comment = 'Compra e venda de ativos'

    def __str__(self):
        return self.id
        
    @property
    def get_values(self):
        valor_total = Decimal(self.valUnitario)*Decimal(self.qtdCotas)
        return valor_total
    
    def save(self, *args, **kwargs):
        self.valTotal = self.get_values
        super(Movimento, self).save(*args, **kwargs)


@receiver(post_save, sender=Movimento)
def atualiza_fii(sender, instance, **kwargs):
    codFii_id = instance.codFii
    fii = Fii.objects.filter(codFii=codFii_id).first() 
    if fii:
        if instance.tipMovimento == "C":
            fii.valTotal = fii.valTotal + instance.valTotal
            fii.qtdCotas = fii.qtdCotas + int(instance.qtdCotas)
        else:
            fii.valTotal = fii.valTotal - instance.valTotal
            fii.qtdCotas = fii.qtdCotas - int(instance.qtdCotas)
        fii.save()
        
@receiver(post_delete, sender=Movimento)
def atualiza_fii_del(sender, instance, **kwargs):
    codFii_id = instance.codFii
    fii = Fii.objects.filter(codFii = codFii_id).first()
    if fii:
        if instance.tipMovimento == "C":
            fii.valTotal = fii.valTotal - instance.valTotal
            fii.qtdCotas = fii.qtdCotas - int(instance.qtdCotas)
        else:
            fii.valTotal = fii.valtotal + instance.valTotal
            fii.qtdCotas = fii.qtdCotas + int(instance.qtdCotas)
        fii.save()