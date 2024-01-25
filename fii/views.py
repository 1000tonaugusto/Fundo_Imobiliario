from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import constants
from .models import Fii
from tipofii.models import Tipofii


def novo_fii(request):
    if request.method == "GET":
        tipofiis = Tipofii.objects.all()
        return render(request, 'novo_fii.html', {'tipofiis': tipofiis })
    elif request.method == "POST":
        codFii = request.POST.get("codFii")
        nomFii = request.POST.get("nomFii")
        datCom = request.POST.get("datCom")
        datPag = request.POST.get("datPag")
        tipFii = request.POST.get("tipFii")
        
        fii = Fii(
            codFii = codFii,
            nomFii = nomFii,
            datCom = datCom,
            datPag = datPag,
            tipFii_id = tipFii,
            qtdCotas = 0,
            valTotal = 0 
        )
        
        fii.save()
        messages.add_message(request, constants.SUCCESS, 'Fundo incluido com sucesso')
        return redirect('/fii/novo_fii/')

def lista_fii(request):
    if request.method == "GET":
        tipofiis = Tipofii.objects.all()
        fiis = Fii.objects.all()
        filtra_fii_nome = request.GET.get('nomFii')
        filtra_fii_tipo = request.GET.get('tipFii')
        
        if filtra_fii_nome:
            fiis = Fii.objects.filter(nomFii__icontains = filtra_fii_nome)
            
        if filtra_fii_tipo:
            fiis = Fii.objects.filter(tipFii=filtra_fii_tipo)
            
        return render(request, 'lista_fii.html', {'fiis': fiis, 'tipofiis': tipofiis })
        
def altera_fii(request, codFii):
    pass

def exclui_fii(request, codFii):
    pass