from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import CustomUserRegistrationForm, CustomAuthenticationForm, ProfileForm
from django.views.generic import DetailView
from .models import News
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

def index(request):
    # first_news = News.objects.filter(is_published=True).order_by('created_at')[:7]
    # context = {
    #
    # }
    # return render(request, 'apphub/index.html', {'news_list': first_news})
    reg_form = CustomUserRegistrationForm()
    login_form = CustomAuthenticationForm(request, data=request.POST or None)
    if request.method == "POST":
        if 'register' in request.POST:
            reg_form = CustomUserRegistrationForm(request.POST)
            if reg_form.is_valid():
                user = reg_form.save(commit=False)
                user.set_password(reg_form.cleaned_data['password'])
                user.save()
                login(request, user)
                messages.success(request, "Регистрация прошла успешно.")
                return redirect('index')

        elif 'login' in request.POST:
            login_form = CustomAuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                messages.success(request, "Вы вошли в систему.")
                return redirect('index')  # замените на нужный маршрут
            else:
                messages.error(request, "Неверный логин или пароль.")

    return render(request, 'apphub/index.html', {
        'reg_form': reg_form,
        'login_form': login_form
    })


def logout_view(request):
    logout(request)
    return redirect("login")


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
    return render(request, 'apphub/profile.html', {'form': form})
