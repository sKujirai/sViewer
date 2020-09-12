from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def crystal(request):
    return render(request, 'crystal.html')
