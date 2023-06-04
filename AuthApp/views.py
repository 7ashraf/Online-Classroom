from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from .forms import *
from .models import *

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        print(request.user.email)
        return redirect(reverse('dashboard:dashboardRouter'))
    else:
        return HttpResponseRedirect('login')

def log_in(request):
    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        
        if loginForm.is_valid():
            email = loginForm.cleaned_data['email']
            password = loginForm.cleaned_data['password']
            user = authenticate(request, email = email, password = password)

            if user is not None :
                login(request, user)
                print(f'Login Successful {user.email}')
                return redirect(reverse('dashboard:dashboardRouter'))
            else :
                print('wrong credentials')
                return render(request, 'login.html', {
                    'form':loginForm
                })
    else:
        loginForm = LoginForm()
        return render(request, 'login.html', {
            'form': loginForm
        })

def log_out(request):
    logout(request)
    return HttpResponseRedirect('/login')

def register(request):
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid:
            user = form.save()

            if user.is_student :
                student = Student(user = user)
                student.save()
            elif user.is_teacher:
                teacher = Teacher(user = user)
                teacher.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(request, email = email, password = password)
            login(request, user)
            return redirect(reverse('dashboard:dashboardRouter'))
    else:
        form = CreateUserForm()    
    ctx = {
        'form' : form
    }

    return render(request,'register.html', ctx)