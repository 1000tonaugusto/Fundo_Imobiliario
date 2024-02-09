from django.db import models


class Tipofii(models.Model):
    nomTipo = models.CharField(max_length=50, verbose_name='Descrição tipo de fundo', default='')
    
    class Meta:
        db_table = 'tipofii'
        db_table_comment = 'Tipo de Fundos imobiliarios'
        
    def __str__(self):
        return self.nomTipo
