from django.urls import path
from . import views


urlpatterns = [
    path('novo_dividendo', views.novo_dividendo, name='novo_dividendo'),
    path('lista_dividendo', views.lista_dividendo, name='lista_dividendo'),
    path('exclui_dividendo/<int:id>', views.exclui_dividendo, name='exclui_dividendo'),
    path('altera_dividendo/<int:id>', views.altera_dividendo, name='altera_dividendo'),
    path('grafico_dividendo/', views.grafico_dividendo, name='grafico_dividendo'),
    path('relatorio_dividendo/', views.relatorio_dividendo, name='relatorio_dividendo'),
    path('resumo_dividendo', views.resumo_dividendo, name='resumo_dividendo'),
]