from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .auth_forms import BootstrapAuthenticationForm
from .forms import RegisterForm
from .models import Profile


def register(request):
    if request.user.is_authenticated:
        return redirect("restaurant:home")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome aboard — your account is ready.")
            if user.profile.role == Profile.Role.OWNER:
                return redirect("restaurant:my_restaurant")
            return redirect("restaurant:home")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    form_class = BootstrapAuthenticationForm
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("restaurant:home")
