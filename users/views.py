from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm #, ProfileUpdateForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User


# Create your views here.

def register(request):
    # if user is already signed in, redirect back to dashboard
    if request.user.is_authenticated:
        messages.success(request, f"You are already signed in!")
        return redirect('dashboard')

    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid() and not User.objects.filter(email=form.cleaned_data.get('email')).exists():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Your account has been created! Please sign in!", )
            return redirect("login")
        else:
            return render(request, 'users/register.html', {'form': form})
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


class LoginFormView(SuccessMessageMixin, LoginView):
    template_name='users/login.html'
    success_message = f"Welcome, you are successfully logged in!"

    def get(self, request, *args, **kwargs):
        # if user is already signed in, redirect back to dashboard
        if request.user.is_authenticated:
            messages.success(request, f"You are already signed in!")
            return redirect('dashboard')
        return super().get(request, *args, **kwargs)

class LogoutFormView(SuccessMessageMixin, LogoutView):
    success_message = f"You have been successfully logged out!"