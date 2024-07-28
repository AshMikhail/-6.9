from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import SignUpForm, UpdateSiteUserForm, UpdateUserForm
from .models import SiteUser


def frontpage(request):
    return render(request, 'accounts/frontpage.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            SiteUser.objects.create(user=user)
            login(request, user)
            return redirect('frontpage')

    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'accounts/frontpage.html')

def profile_view(request):
    context = {
        'user': request.user
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        situeser_form = UpdateSiteUserForm(request.POST, request.FILES, instance=request.user.siteuser)

        if user_form.is_valid() and situeser_form.is_valid():
            user_form.save()
            situeser_form.save()
            return redirect(to='profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        situeser_form = UpdateSiteUserForm(instance=request.user.siteuser)
    return render(request, 'accounts/edit_profil.html', {'user_form': user_form, 'situeser_form': situeser_form})

def AllUsers(request):
    users_list = User.objects.all()

    context = {
            "users_list": users_list,
            "username": User.username,
        }
    return render(request, 'accounts/AllUsers.html', context)