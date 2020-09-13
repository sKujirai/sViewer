from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def mesh(request):
    return render(request, 'mesh.html')
