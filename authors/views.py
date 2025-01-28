from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterForm
from django.contrib.auth.decorators import login_required
from quizmania.models import Profile, User

def register_view(request):
    if request.user.is_authenticated:
        return redirect('quizmania:home')
    else:
        register_form_data = request.session.get('register_form_data', None)
        form = RegisterForm(register_form_data)
        form_action = reverse('authors:register_create')
        request.session.pop('register_form_data', None)
        return render(request, 'authors/pages/register_user.html',{
            'form': form, 
            'form_action':form_action,
            'is_register_page':True,
        })
    

def register_create(request):
    if request.method == 'POST':
        POST = request.POST
        request.session['register_form_data'] = POST
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            profile = Profile.objects.create(user=user)
            profile.save()
            authenticated_user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            messages.success(request, 'Perfil criado com sucesso!')
            login(request, authenticated_user)
            del(request.session['register_form_data'])
            return redirect('authors:login')
        return redirect('authors:register')
    raise Http404

def login_view(request):
    if request.user.is_authenticated:
        return redirect('quizmania:home')
    else:
        form = LoginForm()
        form_action = reverse('authors:login_create')
        return render(request, 'authors/pages/login.html',{
            'form': form,
            'form_action': form_action,
            'is_login_page': True,
        })

def login_create(request):
    if request.method == 'POST':     
        form = LoginForm(request.POST)
        if form.is_valid():
            authenticated_user = authenticate(
                username=form.cleaned_data.get('username', ''),
                password=form.cleaned_data.get('password', '')
            )

            if authenticated_user is not None:
                login(request, authenticated_user)
                messages.success(request, 'Entrou com sucesso!')

            else:
                messages.error(request, 'Credênciais inválidas')
            

        else:
            messages.error(request, 'Nome de usuário ou senha invalidos')
        return redirect('authors:login')
    raise Http404()
    

@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Você saiu com sucesso!') 
        return redirect(reverse('authors:login'))
    return redirect(reverse('quizmania:home'))