import requests, random, json
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.views.generic import ListView, TemplateView, DetailView
from .forms import PrefectureForm, UploadForm, AccountForm, AddAccountForm
from .models import UploadImage, LikeForPost
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# 投稿へのいいね
def like_for_post(request):
    post_pk = request.POST.get('post_pk')
    context = {
        'user': f'{request.user.last_name} {request.user.first_name}',
    }
    post = get_object_or_404(UploadImage, pk=post_pk)
    like = LikeForPost.objects.all().filter(target=post, user=request.user)

    # 既にいいねされてたらいいね消す、されてなかったらいいねする
    if like.exists():
        like.delete()
        post.sum_like -= 1
        post.save()
        context['method'] = 'delete'
    else:
        like.create(target=post, user=request.user)
        post.sum_like += 1
        post.save()
        context['method'] = 'create'
    
    context['like_for_post_count'] = post.likeforpost_set.count()
       
    return JsonResponse(context)


# ホーム画面(ログインなし)
class IndexView(generic.TemplateView):
    model = UploadImage
    
    def __init__(self):
        self.params = {
            "PrefectureList": PrefectureForm,
            "max_temp": 0,
            "min_temp": 0,
            "climate": None,
            "coordinate": None,
            "images": None,
        }

    # Get処理
    def get(self, request):
        # 初期値は東京
        INITIAL_LOCATION = 'lat=35.4122&lon=139.4130'
        self.params = index(self, request, INITIAL_LOCATION)
        
        return render(request, "clothes/index.html", context=self.params)

    # Post処理
    def post(self, request):
        # プルダウンリストから位置取得
        LOCATION = request.POST['choice']
        self.params = index(self, request, LOCATION)
        
        return render(request, "clothes/index.html", context=self.params)
    
    
#ログインボタンを押した
def Login(request):
    # Post処理
    if request.method == 'POST':
        # フォーム入力のユーザーID・パスワード取得
        ID = request.POST.get('userid')
        Pass = request.POST.get('password')

        # Djangoの認証機能
        user = authenticate(username=ID, password=Pass)

        # ユーザー認証
        if user:
            #ユーザーアクティベート判定
            if user.is_active:
                # ログイン
                login(request,user)
                
                return HttpResponseRedirect('home')
            else:
                # アカウント利用不可
                return HttpResponse("アカウントが有効ではありません")
        # ユーザー認証失敗
        else:
            return HttpResponse("ユーザー名またはパスワードが間違っています")
    # Get処理
    else:
        return render(request, 'clothes/login.html')

class ImageList(ListView):
    model = UploadImage
    template_name = 'clothes/image_list.html'

# ホーム画面(ログインあり)
@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    model = UploadImage

    def __init__(self):
        self.params = {
            "PrefectureList": PrefectureForm,
            "max_temp": 0,
            "min_temp": 0,
            "climate": None,
            "coordinate": None,
            "images": None,
        }

    # Get処理
    def get(self, request):
        # 初期値は東京
        INITIAL_LOCATION = 'lat=35.4122&lon=139.4130'
        self.params = home(self, request, INITIAL_LOCATION)
        
        return render(request, "clothes/home.html", context=self.params)

    # Post処理
    def post(self, request):
        # プルダウンリストから位置取得
        LOCATION = request.POST['choice']
        self.params = home(self, request, LOCATION)
        
        return render(request, "clothes/home.html", context=self.params)

#ログアウト
@login_required
def Logout(request):
    logout(request)
    # ログイン画面遷移
    return render(request, 'clothes/logout.html')

#新規登録
class  AccountRegistration(TemplateView):
    def __init__(self):
        self.params = {
        "AccountCreate":False,
        "account_form": AccountForm(),
        "add_account_form":AddAccountForm(),
        }

    #Get処理
    def get(self,request):
        self.params["account_form"] = AccountForm()
        self.params["add_account_form"] = AddAccountForm()
        self.params["AccountCreate"] = False
        return render(request,"clothes/register.html",context=self.params)

    #Post処理
    def post(self,request):
        self.params["account_form"] = AccountForm(data=request.POST)
        self.params["add_account_form"] = AddAccountForm(data=request.POST)

        #フォーム入力の有効検証
        if self.params["account_form"].is_valid() and self.params["add_account_form"].is_valid():
            # アカウント情報をDB保存
            account = self.params["account_form"].save()
            # パスワードをハッシュ化
            account.set_password(account.password)
            # ハッシュ化パスワード更新
            account.save()
            
            # 下記追加情報
            # 下記操作のため、コミットなし
            add_account = self.params["add_account_form"].save(commit=False)
            # AccountForm & AddAccountForm 1vs1 紐付け
            add_account.user = account

            # モデル保存
            add_account.save()

            # アカウント作成情報更新
            self.params["AccountCreate"] = True

        else:
            # フォームが有効でない場合
            print(self.params["account_form"].errors)

        return render(request,"clothes/register.html",context=self.params)

# 画像アップロード
@login_required
def upload(request):
    
    params = {
        'region': PrefectureForm(),
        'upload_form': UploadForm(),
        'temprature': None,
    }

    # Postなら県庁所在地からAPIで気温取得
    if (request.method == 'POST'):
        # APIキー取得
        json_open = open('clothes/openweather_apikey.json', 'r')
        json_load = json.load(json_open)
        API_KEY = json_load['API_KEY']
        LOCATION = request.POST['choice']
        
        # OpenWeatherMapAPIから当日の天気予報取得
        geo_request_url = f"https://api.openweathermap.org/data/2.5/onecall?{LOCATION}&exclude=minutely,current&units=metric&lang=ja&&appid={API_KEY}"
        temperature_data = requests.get(geo_request_url).json()
        max_temp = int(temperature_data['daily'][0]['temp']['max'])
        min_temp = int(temperature_data['daily'][0]['temp']['min'])
        coordinate, temp_num = coordinate_message(max_temp, min_temp)
        params['region'] = PrefectureForm(request.POST)
                
        # 投稿フォーム
        form = UploadForm(request.POST, request.FILES)
        
        # 気温と画像をセットでアップロード
        if form.is_valid():
            upload_image = form.save(commit=False)
            upload_image.temperature = temp_num
            upload_image.user = request.user
            upload_image.save()
            params['id'] = upload_image.id
            
    return render(request, "clothes/upload.html", params)

# マイページ
@method_decorator(login_required, name='dispatch')
class MyPageView(TemplateView):
    template_name = 'clothes/mypage.html'
    model = UploadImage
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # いいねされてるかの有無によって表示変更
        d = {}
        for post in UploadImage.objects.all():
            # いいね数のカウント
            like_for_post_count = post.likeforpost_set.count()
            if post.likeforpost_set.filter(user=self.request.user).exists():
                is_user_liked_for_post = True
            else:
                is_user_liked_for_post = False
            d[post.pk] = {'count': like_for_post_count, 'is_user_liked_for_post': is_user_liked_for_post}
        
        # ログイン中のユーザー名
        context['username'] = self.request.user.username
        context['images'] = UploadImage.objects.filter(user=self.request.user)
        # 辞書として送信
        context[f'post_like_data'] = d
        
        return context

# max_tempとmin_tempから服装提案メッセージ
def coordinate_message(max_temp, min_temp):
    if max_temp >= 23 and min_temp > 20:
        coordinate = '半袖など真夏の格好でいいでしょう'
        temp_num = 7
    elif max_temp >= 23 and min_temp <= 20:
        coordinate = '半袖とプラスで何かはおうものがあるといいでしょう'
        temp_num = 6
    elif 18 <= max_temp < 23 and 16 <= min_temp < 23:
        coordinate = ('薄めカーディガンや長袖シャツを着ていくといいでしょう')
        temp_num = 5
    elif 18 <= max_temp < 23 and 16 > min_temp:
        coordinate = ('厚めのカーディガンやスウェットを着ていくといいでしょう')
        temp_num = 4
    elif 10 <= max_temp < 18 and 8 <= min_temp < 18:
        coordinate = ('セーターや春物のコートを着ていくといいでしょう')
        temp_num = 3
    elif 10 <= max_temp < 18 and 8 > min_temp:
        coordinate = 'トレンチコートなど着ていくといいでしょう'
        temp_num = 2
    elif max_temp < 10 and 2 <= min_temp < 10:
        coordinate = '冬物コートやボアブルゾンを着ていくようにしましょう'
        temp_num = 1
    elif max_temp < 10 and 2 > min_temp:
        coordinate = 'ダウンコートや手袋、マフラーが必須です'
        temp_num = 0
    
    return coordinate, temp_num
   

# index.html用
def index(self, request, location):
    # APIキー取得
    json_open = open('clothes/openweather_apikey.json', 'r')
    json_load = json.load(json_open)
    API_KEY = json_load['API_KEY']
    LOCATION = location
    
    # OpenWeatherMapAPIから当日の天気予報取得
    geo_request_url = f"https://api.openweathermap.org/data/2.5/onecall?{LOCATION}&exclude=minutely,current&units=metric&lang=ja&&appid={API_KEY}"
    temperature_data = requests.get(geo_request_url).json()
    max_temp = int(temperature_data['daily'][0]['temp']['max'])
    min_temp = int(temperature_data['daily'][0]['temp']['min'])
    climate = str(temperature_data['hourly'][5]['weather'][0]['main'])
    coordinate, temp_num = coordinate_message(max_temp, min_temp)
    
    # パラメータに値を入れる
    context = {}
    context['max_temp'] = max_temp
    context['min_temp'] = min_temp
    context['climate'] = climate
    context['coordinate'] = coordinate
    context['images'] = UploadImage.objects.filter(temperature=temp_num).order_by('-sum_like')
    
    # Post用とGet用
    if (request.method == 'POST'):
        context["PrefectureList"] = PrefectureForm(request.POST)
    else:
        context["PrefectureList"] = PrefectureForm()
    
    return context


# home.html用
def home(self, request, location):
        # APIキー取得
        json_open = open('clothes/openweather_apikey.json', 'r')
        json_load = json.load(json_open)
        API_KEY = json_load['API_KEY']
        LOCATION = location
        
        # OpenWeatherMapAPIから当日の天気予報取得
        geo_request_url = f"https://api.openweathermap.org/data/2.5/onecall?{LOCATION}&exclude=minutely,current&units=metric&lang=ja&&appid={API_KEY}"
        temperature_data = requests.get(geo_request_url).json()
        max_temp = int(temperature_data['daily'][0]['temp']['max'])
        min_temp = int(temperature_data['daily'][0]['temp']['min'])
        climate = str(temperature_data['hourly'][5]['weather'][0]['main'])
        coordinate, temp_num = coordinate_message(max_temp, min_temp)
        
        # いいねされてるかの有無によって表示変更
        d = {}
        for post in UploadImage.objects.all():
            if post.likeforpost_set.filter(user=self.request.user).exists():
                is_user_liked_for_post = True
            else:
                is_user_liked_for_post = False
            d[post.pk] = {'is_user_liked_for_post': is_user_liked_for_post}
        
        # パラメータに値を入れる
        context = {}
        context[f'post_like_data'] = d
        context['max_temp'] = max_temp
        context['min_temp'] = min_temp
        context['climate'] = climate
        context['coordinate'] = coordinate
        context['images'] = UploadImage.objects.filter(temperature=temp_num).order_by('-sum_like')
        
        # Post用とGet用
        if (request.method == 'POST'):
            context["PrefectureList"] = PrefectureForm(request.POST)
        else:
            context["PrefectureList"] = PrefectureForm()
        
        return context
