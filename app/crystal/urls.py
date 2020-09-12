from django.urls import path

from . import views
from . import crystal


app_name = 'crystal'
urlpatterns = [
    path('', views.crystal, name='crystal'),
]
