from django.urls import path
from . import views


urlpatterns = [
    path('novo_dividendo', views.novo_dividendo, name='novo_dividendo'),
    path('lista_dividendo', views.lista_dividendo, name='lista_dividendo'),
    path('exclui_dividendo/<int:id>', views.exclui_dividendo, name='exclui_dividendo'),
    path('altera_dividendo/<int:id>', views.altera_dividendo, name='altera_dividendo'),
]
