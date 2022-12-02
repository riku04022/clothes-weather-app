from django.urls import path, include

from . import views # mysite/myapp/views.pyをインポート

from django.contrib.auth import views as auth_views

app_name = 'clothes'
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.Login, name='Login'),
    path('home', views.logindex, name='home'),
    path('logout', views.Logout, name="Logout"),
    path('register', views.AccountRegistration.as_view(), name='register'),
    path('upload', views.post_image, name="post_image"),
    path('login', include('django.contrib.auth.urls')),
]