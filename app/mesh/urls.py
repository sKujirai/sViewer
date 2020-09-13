from django.urls import path

from . import views
from . import mesh


app_name = 'mesh'
urlpatterns = [
    path('', views.mesh, name='mesh'),
]
