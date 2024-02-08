from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.messages import constants

from .models import Fii
from tipofii.models import Tipofii
from dividendo.models import Dividendo
from movimento.models import Movimento


def novo_fii(request):                                                              # Função de inclusao de fundo imobiliário
    if request.method == "GET":                                                     # Trata tipo de requisição GET
        tipofiis = Tipofii.objects.all().order_by('nomTipo')                        # Pesquisa todos os tipos de fundos imobiliarios para povoar o select do html
        return render(request, 'fii/novo_fii.html', {'tipofiis': tipofiis })            # Renderiza o template html
    elif request.method == "POST":                                                  # Trata tipo de requisição POST
        codFii = request.POST.get("codFii")                                         # Recebe codFii do template html
        nomFii = request.POST.get("nomFii")                                         # Recebe nomFii do template html
        datCom = request.POST.get("datCom")                                         # Recebe datCom do template html
        datPag = request.POST.get("datPag")                                         # Recebe datPag do template html
        tipFii = request.POST.get("tipFii")                                         # Recebe tipFii do template html
        
        fii = Fii(                                                                  # cria instancia da model Fii com os dados recebidos do template
            codFii = codFii,
            nomFii = nomFii,
            datCom = datCom,
            datPag = datPag,
            tipFii_id = tipFii,
            qtdCotas = 0,
            valTotal = 0 
        )
        
        fii.save()                                                                  # Salva a informação no banco de dados
        messages.add_message(request, constants.SUCCESS, 'Fundo incluido com sucesso') # Exibe mensagem de inclusão
        return redirect('novo_fii')                                           # Redireciona para inclusão de um novo registro

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
        
def altera_fii(request, codFii):                                                    # Função para alteração de fundos imobiliários
    if request.method == "GET":                                                     # Trata a requisição GET
        tipofiis = Tipofii.objects.all().order_by('nomTipo')                        # Pesquisa tipos de fundos para carregar o select do template html
        fii = Fii.objects.get(codFii=codFii)                                        # Pesquisa fundo imobiliário pelo codigo
        tipoFiiSel = fii.tipFii                                                     # Tipo de fundo que está no cadastro do fundo imobiliário para trazer selecionado no select do template html
        return render(request, 'fii/novo_fii.html', {'fii': fii, 'tipofiis': tipofiis, 'tipofiisel': tipoFiiSel}) 
        
    elif request.method == "POST":                                                  # Trata o metodo POST
        fii = Fii.objects.get(codFii=codFii)   
        fii.codFii = request.POST.get("codFii")                                         # Recebe codFii do template html
        fii.nomFii = request.POST.get("nomFii")                                         # Recebe nomFii do template html
        fii.datCom = request.POST.get("datCom")                                         # Recebe datCom do template html
        fii.datPag = request.POST.get("datPag")                                         # Recebe datPag do template html
        fii.tipFii = request.POST.get("tipFii")    # Pesquisa fundo pelo código
        fii.save()                                                                  # Salva a alteração no banco de dados
        return redirect('lista_fii')                                                # Redireciona para a lista de fundocs imobiliários
    
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