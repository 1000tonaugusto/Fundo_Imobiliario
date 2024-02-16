from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from decimal import Decimal

from .models import Movimento
from fii.models import Fii


@login_required()
def novo_movimento(request):                                                                                        # Função para inclusão de movimentos
    if request.method == "GET":                                                                                     # Trata a requisição GET
        fiis = Fii.objects.all().order_by('codFii')                                                                 # Pesquisa todos os fundo imobiliarios
        tipMovimentos = Movimento.MOVIMENTO_CHOICES
        return render(request,'movimento/novo_movimento.html', {'fiis': fiis, 
                                                                'tipMovimentos': tipMovimentos})                    # Carrega o template html com as informações dos fundos
    elif request.method == "POST":                                                                                  # Trata a requisição POST
        codFii = request.POST.get('codFii')
        datMovimento = request.POST.get('datMovimento')
        qtdCotas = request.POST.get('qtdCotas')
        valUnitario = request.POST.get('valUnitario')
        tipMovimento = request.POST.get('tipMovimento')
        valUnitario = Decimal(valUnitario)
        
        if len(codFii.strip()) == 0 or len(datMovimento.strip()) == 0 or qtdCotas == 0 or valUnitario == 0:
            messages.add_message(request, constants.ERROR, "Preencha todos os campos")
            return redirect('novo_movimento')
        
        movimento = Movimento(codFii_id=codFii, datMovimento=datMovimento, qtdCotas=qtdCotas, valUnitario=valUnitario, tipMovimento=tipMovimento)
        movimento.save()

        messages.add_message(request, constants.SUCCESS, 'Movimento incluído com sucesso!')
        return redirect('novo_movimento')


@login_required()
def lista_movimento(request):
    if request.method == "GET":
        fiis = Fii.objects.all().order_by('codFii')
        movimentos = Movimento.objects.all().order_by('datMovimento')

        filtra_fii = request.GET.get('codFii_filtra')
        if filtra_fii:
            movimentos = Movimento.objects.filter(codFii_id=filtra_fii)
        
        return render(request, 'movimento/lista_movimento.html', {'fiis': fiis, 'movimentos': movimentos})
    
    
@login_required()
def resumo_movimento(request):
    if request.method == "GET":
        fiis = Fii.objects.all().order_by('codFii')
        movimentos = Movimento.objects.all().values('codFii').annotate(quanttotal=Sum('qtdCotas'),valortotal=Sum('valTotal')).order_by('-valTotal')
        
        filtra_fii = request.GET.get('codFii_filtra')
        if filtra_fii:
            movimentos = Movimento.objects.filter(codFii_id=filtra_fii)
        
        return render(request, 'movimento/resumo_movimento.html', {'fiis': fiis, 'movimentos': movimentos})
        


@login_required()
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


@login_required()
def exclui_movimento(request, id):
    movimento = Movimento.objects.get(id=id)
    movimento.delete()
    messages.add_message(request, constants.SUCCESS,'Movimento excluido com sucesso!')
    return redirect('lista_movimento')


@login_required()
def grafico_movimento(request):
    movimentos = Movimento.objects.values_list('codFii').annotate(valor_total=Sum('valTotal'))
    rotulos = [x[0] for x in movimentos]
    valores = [float(x[1]) for x in movimentos]
    
    return render(request, 'movimento/grafico_movimento.html', {'rotulos': rotulos, 'valores': valores})

