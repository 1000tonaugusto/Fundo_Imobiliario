from django.shortcuts import render, redirect
from .models import Tipofii
from django.contrib.messages import constants
from django.contrib import messages


def novo_tipofii(request):                                                      # Define o metodo de inclusão de tipo de fundo imobiliário
    if request.method == "GET":                                                 # Trata o tipo de requisiçao GET (Pesquisa)
        tipofiis = Tipofii.objects.all()                                        # Pesquisa todos os tipos de fundos imobiliarios
        filtro_tipofiis = request.GET.get('filtro_tipofiis')                    # Atribui a variável 'filtro_tipofiis' a informação do formulário
        print(filtro_tipofiis)
        if filtro_tipofiis:                                                     # Se for informado no campo de pesquisa do formulário
            tipofiis = tipofiis.filter(id = filtro_tipofiis) # Faz o filtro pela informação digitada no formulário
        return render(request, 'novo_tipofii.html', {'tipofiis': tipofiis})     # Renderiza o arquivo html com a informação dos tipos de fundos imobiliários
    
    elif request.method == "POST":                                              # Trata o tipo de requisiçao POST 
        nomTipo = request.POST.get('nomTipo')                                   # Pega a de nome informação do tipo de fundo do formulário html
        if len(nomTipo.strip()) == 0:                                           # Testa se foi digitado algo no campo de nome do tipo de fundo
            messages.add_message(request, constants.ERROR, 'Preencha o campo de tipo de fundo') # Mensagem para o usuário
            return redirect('/tipofii/novo_tipofii.html')                       # Redireciona para que seja informado o nome do tipo de fundo
        tipofii = Tipofii(nomTipo = nomTipo)                                    # Atribui a informação do nome do tipo de fundo a variável (tipofii)
        tipofii.save()                                                          # Salva a informação no banco de dados
        messages.add_message(request, constants.SUCCESS, 'Tipo de fundo cadastrado com sucesso') # Mensagem para o usuário
        return redirect('/tipofii/novo_tipofii')                                # Redireciona para o formulário html de inclusão
# Fim do metodo de inclusão
    
def exclui_tipofii(request, id):                                                 # Define metodo de exclusão de tipo de fundo imobiliário
    tipofii = Tipofii.objects.get(id=id)                                        # Pesquisa tipo de fundo a ser excluido pelo id
    tipofii.delete()                                                            # Faz a exclusão do banco de dados
    messages.add_message(request, constants.SUCCESS, 'Tipo de fundo excluido com sucesso') # Mensagem para o usuário informando da exclusão
    return redirect('/tipofii/novo_tipofii/')
# Fim do metodo de exclusão