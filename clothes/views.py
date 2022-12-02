from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .forms import PrefectureForm
import requests
from .forms import UploadForm
from .models import UploadImage
import random

from django.views.generic import TemplateView #テンプレートタグ
from .forms import AccountForm, AddAccountForm #ユーザーアカウントフォーム

# ログイン・ログアウト処理に利用
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def index(request):

    prefecture = ""
    max_celsius = ""
    min_celsius = ""
    coordinate = ""
    
    
    if (request.method == 'POST'):
        if('choice' in request.POST):
            location_num = request.POST['choice']

            geo_request_url = f"https://weather.tsukumijima.net/api/forecast/city/{location_num}"
            data = requests.get(geo_request_url).json()
            max_temp = int(data['forecasts'][1]['temperature']['max']['celsius'])
            min_temp = int(data['forecasts'][1]['temperature']['min']['celsius'])
            max_celsius = str(max_temp) + "℃"
            min_celsius = str(min_temp) + "℃"

            if max_temp >= 23 and min_temp > 20:
                coordinate = '半袖など真夏の格好でいいでしょう'
            elif max_temp >= 23 and min_temp <= 20:
                coordinate = '半袖とプラスで何かはおうものがあるといいでしょう'
            elif 18 <= max_temp < 23 and 16 <= min_temp < 23:
                coordinate = ('薄めカーディガンや長袖シャツを着ていくといいでしょう')
            elif 18 <= max_temp < 23 and 16 > min_temp:
                coordinate = ('厚めのカーディガンやスウェットを着ると過ごしやすいでしょう')
            elif 10 <= max_temp < 18 and 8 <= min_temp < 18:
                coordinate = ('セーターや春物のコートを着ていくといいでしょう')
            elif 10 <= max_temp < 18 and 8 > min_temp:
                coordinate = 'トレンチコートなど着ていくといいでしょう'
            elif max_temp < 10 and 2 <= min_temp < 10:
                coordinate = '冬物コートやボアブルゾンを着ていくようにしましょう'
            elif max_temp < 10 and 2 > min_temp:
                coordinate = 'ダウンコートや手袋やマフラーが必須ですね'

    params = {
        'region': prefecture,
        'max': max_celsius,
        'min': min_celsius,
        'coodinate': coordinate,
        'form': PrefectureForm
    }
    
    params['region'] = PrefectureForm(request.POST)
    
    return render(request, 'clothes/index.html' ,params)

def go_Login(request):
    return render(request, 'clothes/login.html')


#ログインボタンを押した
def Login(request):
    # POST
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
    # GET
    else:
        return render(request, 'clothes/login.html')

@login_required
def logindex(request):
    
    prefecture = ""
    max_celsius = ""
    min_celsius = ""
    coordinate = ""
    temp = 0
    list_imageid = []
    url_ = []
    
    params = {
        'region': prefecture,
        'max': max_celsius,
        'min': min_celsius,
        'coodinate': coordinate,
        'form': PrefectureForm,
        'url_1': None,
        'url_2': None,
        'url_3': None,
        'url_4': None,
    }
    
    params['region'] = PrefectureForm(request.POST)
    
    
    if (request.method == 'POST'):
        if('choice' in request.POST):
            location_num = request.POST['choice']

            geo_request_url = f"https://weather.tsukumijima.net/api/forecast/city/{location_num}"
            data = requests.get(geo_request_url).json()
            max_temp = int(data['forecasts'][1]['temperature']['max']['celsius'])
            min_temp = int(data['forecasts'][1]['temperature']['min']['celsius'])
            params['max'] = str(max_temp) + "℃"
            params['min'] = str(min_temp) + "℃"

            if max_temp >= 23 and min_temp > 20:
                params['coordinate'] = '半袖など真夏の格好でいいでしょう'
                temp = 0
            elif max_temp >= 23 and min_temp <= 20:
                params['coordinate'] = '半袖とプラスで何かはおうものがあるといいでしょう'
                temp = 1
            elif 18 <= max_temp < 23 and 16 <= min_temp < 23:
                params['coordinate'] = ('薄めカーディガンや長袖シャツを着ていくといいでしょう')
                temp = 2
            elif 18 <= max_temp < 23 and 16 > min_temp:
                params['coordinate'] = ('厚めのカーディガンやスウェットを着ると過ごしやすいでしょう')
                temp = 3
            elif 10 <= max_temp < 18 and 8 <= min_temp < 18:
                params['coordinate'] = ('セーターや春物のコートを着ていくといいでしょう')
                temp = 4
            elif 10 <= max_temp < 18 and 8 > min_temp:
                params['coordinate'] = 'トレンチコートなど着ていくといいでしょう'
                temp = 5
            elif max_temp < 10 and 2 <= min_temp < 10:
                params['coordinate'] = '冬物コートやボアブルゾンを着ていくようにしましょう'
                temp = 6
            elif max_temp < 10 and 2 > min_temp:
                params['coordinate'] = 'ダウンコートや手袋やマフラーが必須ですね'
                temp = 7
            
            # temprature=tempの画像のidをリストlist_imageidに入れて、指定数分のidをrandom_imageidに入れる
            temp_image = UploadImage.objects.values('image_id').filter(temprature=temp)
            for i in range(len(temp_image)):
                list_imageid.append(temp_image[i]['image_id'])
            ramdom_imageid = random.sample(list_imageid, 2)
            
            for j in ramdom_imageid:
                upload_image = get_object_or_404(UploadImage, id=j)
                url_.append(upload_image.image.url)
            
            params['url_1'] = url_[0]
            params['url_2'] = url_[1]
    
    return render(request, 'clothes/logindex.html' ,params)

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
def post_image(request):
    prefecture = ""
    
    params = {
        'region': prefecture,
        'upload_form': UploadForm(),
        'temprature': None,
        'id': None,
    }
    
    params['region'] = PrefectureForm(request.POST)

    if (request.method == 'POST'):
        if('choice' in request.POST):
            location_num = request.POST['choice']

            geo_request_url = f"https://weather.tsukumijima.net/api/forecast/city/{location_num}"
            data = requests.get(geo_request_url).json()
            max_temp = int(data['forecasts'][1]['temperature']['max']['celsius'])
            min_temp = int(data['forecasts'][1]['temperature']['min']['celsius'])

            if max_temp >= 23 and min_temp > 20:
                temp = 0
            elif max_temp >= 23 and min_temp <= 20:
                temp = 1
            elif 18 <= max_temp < 23 and 16 <= min_temp < 23:
                temp = 2
            elif 18 <= max_temp < 23 and 16 > min_temp:
                temp = 3
            elif 10 <= max_temp < 18 and 8 <= min_temp < 18:
                temp = 4
            elif 10 <= max_temp < 18 and 8 > min_temp:
                temp = 5
            elif max_temp < 10 and 2 <= min_temp < 10:
                temp = 6
            elif max_temp < 10 and 2 > min_temp:
                temp = 7
                
        form = UploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            upload_image = form.save()
            image = UploadImage.objects.get(id=upload_image.id)
            image.temprature = temp
            image.image_id = upload_image.id
            image.save()
            
            params['id'] = upload_image.id
            

    return render(request, "clothes/post_image.html", params)
