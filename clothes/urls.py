from django.urls import path

from . import views

app_name = 'clothes'
urlpatterns = [
    path('', views.index, name='index'),
]