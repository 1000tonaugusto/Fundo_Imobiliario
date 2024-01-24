from django.urls import path
from . import views

urlpatterns = [
    path('novo_tipofii/', views.novo_tipofii, name='novo_tipofii'),
    #path('altera_tipofii/<int:id>', views.altera_tipo, name='altera_tipo'),
    path('exclui_tipofii/<int:id>', views.exclui_tipofii, name='exclui_tipofii'),
    #path('lista_tipofii/', views.lista_tipo, name='lista_tipo'),
]
