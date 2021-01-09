from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm #, ProfileUpdateForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView


# Create your views here.

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Your account has been created! Please sign in!", )
            return redirect("login")
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


class LoginFormView(SuccessMessageMixin, LoginView):
    template_name='users/login.html'
    success_message = f"Welcome, you are successfully logged in!"


class LogoutFormView(SuccessMessageMixin, LogoutView):
    success_message = f"You have been successfully logged out!"