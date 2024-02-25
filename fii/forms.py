from django.forms import ModelForm, TextInput

from .models import Fii

class FiiForm(ModelForm):
    class Meta:
        model = Fii
        fields = ['codFii', 'nomFii', 'datCom', 'datPag', 'tipFii', 'codCor']