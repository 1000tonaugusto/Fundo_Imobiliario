from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm


@login_required
def home(request):
    return render(request,'index.html')

def logout_user(request):
    logout(request)
    return redirect('logar')


class UserLoginView(LoginView):
    template_name='usuario/login.html'
    form = AuthenticationForm

