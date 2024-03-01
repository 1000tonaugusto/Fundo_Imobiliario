from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth

from .models import Movimento
from .forms import MovimentoForm
from fii.models import Fii


@login_required()
def novo_movimento(request):                                                                                        # Função para inclusão de movimentos
    form = MovimentoForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.add_message(request, constants.SUCCESS, 'Movimento incluso com sucesso')
            return redirect('novo_movimento')
    return render(request,'movimento/novo_movimento.html', {'form': form})


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
        rotulos = []
        series = ''
        tipograf = ''
        fiis = Fii.objects.all().order_by('codFii')
        cod_fiis = [i.codFii for i in fiis]
        for i in cod_fiis:
            rotulos.append(i)
            tipograf = tipograf + '{"type": "bar"},'
            dados = []
            dados.append(i)
            x = 1
            while (x <= 12):
                mov = Movimento.objects.annotate(mes=TruncMonth('datMovimento')).values('mes').filter(datMovimento__month=x).filter(codFii=i).annotate(valortotal=Sum('valTotal'))
                if mov:
                    dados.append(float(mov[0]["valortotal"]))
                else:
                    dados.append(0)
                x += 1
            series = series + str(dados) + ','
        series = series[:-1]
        series = series.strip('"\'')
        tipograf = tipograf[:-1]
        print(tipograf)
        
        return render(request, 'movimento/grafico_movimento.html', {'fiis': fiis, 'rotulos': rotulos, 'series': series, 'tipograf': tipograf})


@login_required()
def altera_movimento(request, id):
    movimento = get_object_or_404(Movimento, id=id)
    form = MovimentoForm(request.POST or None, instance=movimento)
    if form.is_valid():
        form.save()
        messages.add_message(request, constants.SUCCESS, 'Movimento atualizado com sucesso')
        return redirect('lista_movimento')
    return render(request, 'movimento/novo_movimento.html', {'form': form})


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

