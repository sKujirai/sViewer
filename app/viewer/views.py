from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def crystal(request):
    return render(request, 'crystal.html')
