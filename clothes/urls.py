from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_views

app_name = 'clothes'
urlpatterns = [
    # トップページへ
    path('', views.IndexView.as_view(), name='index'),
    # ログイン画面へ
    path('login', views.Login, name='Login'),
    # ログイン後のホーム画面へ
    path('home', views.HomeView.as_view(), name='home'),
    # ログアウト後画面へ
    path('logout', views.Logout, name="Logout"),
    # 新規ユーザー登録画面へ
    path('register', views.AccountRegistration.as_view(), name='register'),
    # 画像アップロード画面へ
    path('upload', views.upload, name='upload'),
    # マイページへ
    path('mypage', views.MyPageView.as_view(), name='mypage'),
    # ユーザー認証用
    path('login', include('django.contrib.auth.urls')),
    # いいね
    path('like_for_post', views.like_for_post, name='like_for_post'),
]
