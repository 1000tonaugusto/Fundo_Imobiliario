from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('logar', views.UserLoginView.as_view(), name='logar'),
    path('sair', views.logout_user, name='sair'),
    path('home', views.home, name='home'),
]
