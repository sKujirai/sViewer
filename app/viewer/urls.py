from django.urls import path

from . import views
from . import crystal


app_name = 'viewer'
urlpatterns = [
    path('', views.index, name='index'),
    path('crystal/', views.crystal, name='crystal'),
]
