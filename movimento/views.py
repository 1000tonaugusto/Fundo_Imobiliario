from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.messages import constants
import datetime

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
    if request.method == "GET":
        fiis = Fii.objects.all().order_by('codFii')
        movimentos = Movimento.objects.all().order_by('datMovimento')

        filtra_fii = request.GET.get('codFii_filtra')
        if filtra_fii:
            movimentos = Movimento.objects.filter(codFii_id=filtra_fii)
        
        return render(request, 'movimento/lista_movimento.html', {'fiis': fiis, 'movimentos': movimentos})

def altera_movimento(request, id):
    if request.method == "GET":
        tipMovimentos = Movimento.MOVIMENTO_CHOICES
        movimento = Movimento.objects.get(id=id)
        return render(request, 'movimento/novo_movimento.html', {'movimento': movimento, 'tipMovimentos': tipMovimentos})
    elif request.method == "POST":
        movimento = Movimento.objects.get(id=id)
        movimento.codFii_id = request.POST.get('codFii')
        movimento.datMovimento = request.POST.get('datMovimento')
        movimento.qtdCotas = request.POST.get('qtdCotas')
        movimento.valUnitario = request.POST.get('valUnitario')
        movimento.tipMovimento = request.POST.get('tipMovimento')
        movimento.save()
        return redirect('lista_movimento')

def exclui_movimento(request, id):
    movimento = Movimento.objects.get(id=id)
    movimento.delete()
    messages.add_message(request, constants.SUCCESS,'Movimento excluido com sucesso!')
    return redirect('lista_movimento')

