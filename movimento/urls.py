from django.urls import path
from . import views


urlpatterns = [
    path('novo_movimento/', views.novo_movimento, name='novo_movimento'),
    path('lista_movimento/', views.lista_movimento, name='lista_movimento'),
    path('exclui_movimento/<int:id>', views.exclui_movimento, name='exclui_movimento'),
    path('altera_movimento/<int:id>', views.altera_movimento, name='altera_movimento'),
    path('resumo_movimento/', views.resumo_movimento, name='resumo_movimento'),
    path('grafico_movimento', views.grafico_movimento, name='grafico_movimento'),
]
