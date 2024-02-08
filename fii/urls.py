from django.urls import path
from . import views


urlpatterns = [
    path('novo_fii/', views.novo_fii, name='novo_fii'),
    path('lista_fii/', views.lista_fii, name='lista_fii'),
    path('exclui_fii/<str:codFii>', views.exclui_fii, name='exclui_fii'),
    path('altera_fii/<str:codFii>', views.altera_fii, name='altera_fii'),
]
