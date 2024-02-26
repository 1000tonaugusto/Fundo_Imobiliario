from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.decorators import login_required

from .models import Fii
from .forms import FiiForm
from tipofii.models import Tipofii
from dividendo.models import Dividendo
from movimento.models import Movimento


@login_required()
def novo_fii(request):                                                              # Função de inclusao de fundo imobiliário
    form = FiiForm(request.POST or None)
    if request.method == "POST":
        form = FiiForm(request.POST)
        if form.is_valid():
            form.save()                                                                  # Salva a informação no banco de dados
            messages.add_message(request, constants.SUCCESS, 'Fundo incluido com sucesso') # Exibe mensagem de inclusão
            return redirect('novo_fii')
    return render(request, 'fii/novo_fii.html', {'form': form})


@login_required()
def lista_fii(request):                                                             # Função de lista de fundos imobiliários
    if request.method == "GET":                                                     # Trata o metodo GET
        tipofiis = Tipofii.objects.all()                                            # Pesquisa todos os tipos de fundos imobiliarios para povoar o select do html
        fiis = Fii.objects.all().order_by('nomFii')                                 # Pesquisa todos os fundos imobiliário para preenchar a lista no template html
        filtra_fii_nome = request.GET.get('nomFii')                                 # Recebe a informação do template html para filtro
        filtra_fii_tipo = request.GET.get('tipFii')                                 # Recebe a informação do template html para filtro

        if filtra_fii_nome:                                                         # Se informado o campo de nome do fundo para pesquisa
            fiis = Fii.objects.filter(nomFii__icontains = filtra_fii_nome)          # Faz a pesquisa pelo nome do fundo imobiliário
            
        if filtra_fii_tipo:                                                         # Se for escolhido um tipo de fundo imobiliário
            fiis = Fii.objects.filter(tipFii=filtra_fii_tipo)                       # Faz a pesquisa pelo tipo de fundo imobiliário
            
        return render(request, 'fii/lista_fii.html', {'fiis': fiis, 'tipofiis': tipofiis }) # Renderiza o template html com as informações


@login_required()        
def altera_fii(request, codFii):                                                    # Função para alteração de fundos imobiliários
    fii = get_object_or_404(Fii, codFii=codFii)
    form = FiiForm(request.POST or None, instance=fii)
    if form.is_valid():
        form.save()
        messages.add_message(request, constants.SUCCESS, 'Fundo alterado com sucesso')
        return redirect('lista_fii')
    return render(request, 'fii/novo_fii.html', {'form': form})


@login_required()
def exclui_fii(request, codFii):                                                    # Metodo para exclusão do fundo imobiliário
    fii = Fii.objects.get(codFii=codFii)                                            # Pesquisa fundo imobiliário pelo codigo do fundo
    dividendo = Dividendo.objects.filter(codFii=codFii)[:1]
    if dividendo:
        messages.add_message(request, constants.INFO, 'Não pode excluir, há dividendos para esse fundo')
    else:
        movimento = Movimento.objects.filter(codFii=codFii)[:1]
        if movimento:
            messages.add_message(request, constants.INFO,'Não pode excluir, há compras/vendas para esse fundo')
        else:
            fii.delete()                                                                    # Exclui o fundo imobiliário
            messages.add_message(request, constants.SUCCESS, 'Fundo excluido com sucesso')  # Exibe mensagem informando a exclusão do fundo imobiliário
    return redirect('lista_fii')                                                    # Redireciona para a lista de fundos imobiliários