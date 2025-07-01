from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpRequest

def register_view(request: HttpRequest):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user: User = form.save()
            login(request, user)  # Automatically log in new user
            next_url = request.POST.get("next") or "home"
            return redirect(next_url)
    else:
        form = UserCreationForm()

    context = {
        "form": form,
        "next": request.GET.get("next", ""),
    }
    return render(request, "authentication/register.html", context)
