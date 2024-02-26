from django.forms import ModelForm, DateInput, NumberInput, DecimalField, IntegerField

from .models import Movimento


class MovimentoForm(ModelForm):
    class Meta:
        model = Movimento
        fields = ['codFii', 'datMovimento', 'qtdCotas', 'valUnitario', 'tipMovimento']
        widgets = {'datMovimento': DateInput(format=('%d-%m-%Y'),
                                             attrs={'type':'date'}),
                   'qtdCotas': NumberInput(attrs={'type': 'number'}),}