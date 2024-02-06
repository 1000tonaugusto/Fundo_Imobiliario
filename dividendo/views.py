from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.messages import constants
from decimal import Decimal
import datetime

from .models import Dividendo
from fii.models import Fii


def novo_dividendo(request):
    if request.method == "GET":
        fiis = Fii.objects.all().order_by('codFii')
        return render(request, 'dividendo/novo_dividendo.html', {'fiis': fiis})
    elif request.method == "POST":
        datPaga = request.POST.get('datPaga')
        qtdCotas = request.POST.get("qtdCotas")
        valUnitario = request.POST.get("valUnitario")
        codFii = request.POST.get("codFii")
        valTotal=(Decimal(valUnitario)*Decimal(qtdCotas))
        
        if len(codFii.strip()) == 0 or len(datPaga.strip()) == 0 or len(qtdCotas.strip()) == 0 or len(valUnitario.strip()) == 0:
            messages.add_message(request, constants.ERROR, "Preencha todos os campos")
            return redirect('novo_dividendo')
        
        dividendo = Dividendo(codFii_id=codFii, datPaga=datPaga, qtdCotas=qtdCotas, valUnitario=valUnitario, valTotal=valTotal)
        dividendo.save()
        
        messages.add_message(request, constants.SUCCESS, 'Dividendo incluso com sucesso!')
        return redirect('novo_dividendo')

def lista_dividendo(request):
    if request.method == "GET":
        fiis = Fii.objects.all().order_by('codFii')
        dividendos = Dividendo.objects.all().order_by('datPaga')
        
        filtra_fii = request.GET.get('codFii_filtra')
        if filtra_fii:
            dividendos = Dividendo.objects.filter(codFii_id=filtra_fii)
            
        return render(request, 'dividendo/lista_dividendo.html', {'fiis': fiis, 'dividendos': dividendos})

def altera_dividendo(request, id):
    dividendo = Dividendo.objects.get(id=id)
    if request.method == "GET":
        return render(request, 'dividendo/novo_dividendo.html', {'dividendo': dividendo})
    elif request.method == "POST":
        dividendo.datPaga = request.POST.get('datPaga')
        dividendo.qtdCotas = request.POST.get("qtdCotas")
        dividendo.valUnitario = request.POST.get("valUnitario")
        dividendo.codFii_id = request.POST.get("codFii")
        
        dividendo.save()
        return redirect('lista_dividendo')

def exclui_dividendo(request, id):
    dividendo = Dividendo.objects.get(id=id)
    dividendo.delete()
    messages.add_message(request, constants.SUCCESS, 'Dividendo excluido com sucesso!')
    return redirect('lista_dividendo')
