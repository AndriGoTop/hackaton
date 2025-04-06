from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import CustomUserRegistrationForm, CustomAuthenticationForm, ProfileForm
from .models import News, Subs
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404


def index(request):
    news_list = News.objects.all()
    reg_form = CustomUserRegistrationForm()
    login_form = CustomAuthenticationForm(request, data=request.POST or None)
    if request.method == "POST":
        if 'register' in request.POST:
            reg_form = CustomUserRegistrationForm(request.POST)
            if reg_form.is_valid():
                user = reg_form.save(commit=False)

                user.set_password(reg_form.cleaned_data['password1'])
                print(reg_form.errors)
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
                return redirect('index')
            else:
                messages.error(request, "Неверный логин или пароль.")

    return render(request, 'apphub/index.html', {
        'reg_form': reg_form,
        'login_form': login_form,
        'news_list': news_list,
    })


def logout_view(request):
    logout(request)
    return redirect("index")


def NewsDetailView(request, pk):
    news_list = get_object_or_404(News, pk=pk)
    return render(request, 'apphub/new_details.html', {'news_list': news_list})


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
