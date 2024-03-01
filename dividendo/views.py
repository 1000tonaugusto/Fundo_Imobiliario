from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import constants
from decimal import Decimal
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.db.models.functions import TruncMonth

from .models import Dividendo
from fii.models import Fii


@login_required()
def novo_dividendo(request):
    if request.method == "GET":                                                                     
        fiis = Fii.objects.all().order_by('codFii')
        return render(request, 'dividendo/novo_dividendo.html', {'fiis': fiis})
    elif request.method == "POST":
        datPaga = request.POST.get('datPaga')
        qtdCotas = request.POST.get("qtdCotas")
        valUnitario = request.POST.get("valUnitario")
        codFii = request.POST.get("codFii")
        valUnitario = Decimal(valUnitario)
        
        if len(codFii.strip()) == 0 or len(datPaga.strip()) == 0 or len(qtdCotas.strip()) == 0:
            messages.add_message(request, constants.ERROR, "Preencha todos os campos")
            return redirect('novo_dividendo')
        
        dividendo = Dividendo(codFii_id=codFii, datPaga=datPaga, qtdCotas=qtdCotas, valUnitario=valUnitario)
        dividendo.save()
        
        messages.add_message(request, constants.SUCCESS, 'Dividendo incluso com sucesso!')
        return redirect('novo_dividendo')


@login_required()
def lista_dividendo(request):
    if request.method == "GET":
        fiis = Fii.objects.all().order_by('codFii')
        dividendos = Dividendo.objects.all().order_by('-datPaga')
        
        filtra_fii = request.GET.get('codFii_filtra')
        if filtra_fii:
            dividendos = Dividendo.objects.filter(codFii_id=filtra_fii)
            
        return render(request, 'dividendo/lista_dividendo.html', {'dividendos': dividendos})
    

@login_required()
def resumo_dividendo(request):
    if request.method == "GET":
        fiis = Fii.objects.all().order_by('codFii')
        dividendos = Dividendo.objects.all().values('codFii').annotate(valorTotal=Sum('valTotal'))
        print(fiis)
        filtra_fii = request.GET.get('codFii_filtra')
        if filtra_fii:
            dividendos = Dividendo.objects.filter(codFii_id=filtra_fii)
            
        return render(request, 'dividendo/resumo_dividendo.html', {'fiis': fiis, 'dividendos': dividendos })


@login_required()
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


@login_required()
def exclui_dividendo(request, id):
    dividendo = Dividendo.objects.get(id=id)
    dividendo.delete()
    messages.add_message(request, constants.SUCCESS, 'Dividendo excluido com sucesso!')
    return redirect('lista_dividendo')


@login_required()
def grafico_dividendo(request):
    if request.method == "GET":
        rotulos = []
        series = ''
        
        fiis = Fii.objects.all().order_by('codFii')
        cod_fiis = [i.codFii for i in fiis]
        for i in cod_fiis:
            rotulos.append(i)
            
            dados = []
            dados.append(i)
            x = 1
            tipograf = ''
            while (x <= 12):
                tipograf = tipograf + '{"type": "bar"},'
                mov = Dividendo.objects.annotate(mes=TruncMonth('datPaga')).values('mes').filter(datPaga__month=x).filter(codFii=i).annotate(valortotal=Sum('valTotal'))
                if mov:
                    dados.append(float(mov[0]["valortotal"]))
                else:
                    dados.append(0)
                x += 1
            series = series + str(dados) + ','
        series = series[:-1]
        series = series.strip('"\'')
        tipograf = tipograf[:-1]

        return render(request, 'dividendo/grafico_dividendo.html', {'rotulos': rotulos, 'series': series, 'tipograf': tipograf})
    
    #dividendos = Dividendo.objects.values_list('codFii').annotate(valor_total=Sum('valTotal'))
    #rotulos = []
    #valores = []
    #valores = [x[1] for x in dividendos]
    
    #for dividendo in dividendos:
    #    rotulos.append(dividendo[0])
    #    valores.append(float(dividendo[1]))
    
    #return render(request, 'dividendo/grafico_dividendo.html', {'valores': valores, 'rotulos': rotulos})


@login_required()
def relatorio_dividendo(request):
    dividendos = Dividendo.objects.all().values("codFii","datPaga__year","datPaga__month").annotate(valorTotal=(Sum('valTotal')))[:1]

    return HttpResponse('teste')