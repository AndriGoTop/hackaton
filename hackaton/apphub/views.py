from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import CustomUserRegistrationForm, CustomAuthenticationForm, ProfileForm
from django.views.generic import DetailView
from .models import News
from django.contrib.auth.decorators import login_required


def index(request):
    first_news = News.objects.filter(is_published=True).order_by('created_at')[:6]
    context = {

    }
    return render(request, 'apphub/index.html', {'news_list': first_news})


def logout_view(request):
    logout(request)
    return redirect("login")


def register_view(request):
    if request.method == "POST":
        form = CustomUserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = CustomUserRegistrationForm()
        return render(request, "main/register.html", {'form': form})


def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = CustomUserRegistrationForm()
        return render(request, "main/login.html", {'form': form})


class NewsDetailView(DetailView):
    model = News
    template_name = 'news_detail.html'
    context_object_name = 'news'


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'main/profile.html', {'form': form})
