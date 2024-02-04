from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.messages import constants

from .models import Movimento
from fii.models import Fii


def novo_movimento(request):
    if request.method == "GET":
        fiis = Fii.objects.all().order_by('codFii')
        tipMovimentos = Movimento.MOVIMENTO_CHOICES
        return render(request,'movimento/novo_movimento.html', {'fiis': fiis, 'tipMovimentos': tipMovimentos})
    elif request.method == "POST":
        codFii = request.POST.get('codFii')
        datMovimento = request.POST.get('datMovimento')
        qtdCotas = request.POST.get('qtdCotas')
        valUnitario = request.POST.get('valUnitario')
        tipMovimento = request.POST.get('tipMovimento')

        if len(codFii.strip()) == 0 or len(datMovimento.strip()) == 0 or len(qtdCotas.strip()) == 0 or len(valUnitario.strip()) == 0:
            messages.add_message(request, constants.ERROR, "Preencha todos os campos")
            return redirect('novo_movimento')
        
        movimento = Movimento(codFii_id=codFii, datMovimento=datMovimento, qtdCotas=qtdCotas, valUnitario=valUnitario, tipMovimento=tipMovimento)
        movimento.save()

        messages.add_message(request, constants.SUCCESS, 'Movimento incluído com sucesso!')
        return redirect('novo_movimento')

def lista_movimento(request):
    pass

def altera_movimento(request, id):
    pass

def exclui_movimento(request, id):
    pass

