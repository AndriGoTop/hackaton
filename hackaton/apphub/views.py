from django.shortcuts import render

def index(request):
    context = {

    }
    return render(request, 'apphub/index.html', context)
