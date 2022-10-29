from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .forms import PrefectureForm
import requests

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
    
    
    
    template = loader.get_template('clothes/index.html')
    
    return HttpResponse(template.render(params, request))



