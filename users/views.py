from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login as auth_log
from django.contrib.auth.decorators import login_required
from django.template import context
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserRegisterForm, UserSettingsForm,UserLoginForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login(request):
    if request.method=='POST':
        form=UserLoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(request,username=username,password=password)
            if user is not None:
                auth_log(request,user)
                return redirect('home')
            else:
                form.add_error(None,'invalide name or password')
    else:
        form=UserLoginForm()
    context={'form':form}
    return render(request,'users/login.html',context)


@login_required
def account_settings(request):
    if request.method == 'POST':
        u_form = UserSettingsForm(request.POST, instance=request.user)
        p_form = PasswordChangeForm(request.user, request.POST)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            user = p_form.save()
            update_session_auth_hash(request, user)  # Keeps the user logged in after password change
            return redirect('account_settings')
    else:
        u_form = UserSettingsForm(instance=request.user)
        p_form = PasswordChangeForm(request.user)

    context = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'users/settings.html', context)


def home(request):
    return render(request,'users/home.html')
