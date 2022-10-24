from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
import requests


def index(request):
    # エリアコード
    area_dic = {'Hokkaido':'016010',
                'Aomori':'020010',
                'Iwate':'030010',
                'Miyagi':'040010',
                'Akita':'050010',
                'Yamagata':'060010',
                'Fukushima':'070010',
                'Ibaraki':'080010',
                'Tochigi':'090010',
                'Gunma':'100010',
                'Saitama':'110010',
                'Chiba':'120010',
                'Tokyo':'130010',
                'Kanagawa':'140010',
                'Niigata':'150010',
                'Toyama':'160010',
                'Ishikawa':'170010',
                'Fukui':'180010',
                'Yamanashi':'190010',
                'Nagano':'200010',
                'Gifu':'210010',
                'Shizuoka':'220010',
                'Aichi':'230010',
                'Mie':'240010',
                'Shiga':'250010',
                'Kyoto':'260010',
                'Osaka':'270010',
                'Hyogo':'280010',
                'Nara':'290010',
                'Wakayama':'300010',
                'Tottori':'310010',
                'Shimane':'320010',
                'Okayama':'330010',
                'Hiroshima':'340010',
                'Yamaguchi':'350010',
                'Tokushima':'360010',
                'Kagawa':'370010',
                'Ehime':'380010',
                'Kochi':'390010',
                'Fukuoka':'400010',
                'Saga':'410010',
                'Nagasaki':'420010',
                'Kumamoto':'430010',
                'Oita':'440010',
                'Miyazaki':'450010',
                'Kagoshima':'460010',
                'Okinawa':'471010',
                }
    
    # 漢字変換用
    area_prefecture = {'Hokkaido':'北海道',
                'Aomori':'青森県',
                'Iwate':'岩手県',
                'Miyagi':'宮城県',
                'Akita':'秋田県',
                'Yamagata':'山形県',
                'Fukushima':'福島県',
                'Ibaraki':'茨城県',
                'Tochigi':'栃木県',
                'Gunma':'群馬県',
                'Saitama':'埼玉県',
                'Chiba':'千葉県',
                'Tokyo':'東京都',
                'Kanagawa':'神奈川県',
                'Niigata':'新潟県',
                'Toyama':'富山県',
                'Ishikawa':'石川県',
                'Fukui':'福井県',
                'Yamanashi':'山梨県',
                'Nagano':'長野県',
                'Gifu':'岐阜県',
                'Shizuoka':'静岡県',
                'Aichi':'愛知県',
                'Mie':'三重県',
                'Shiga':'滋賀県',
                'Kyoto':'京都府',
                'Osaka':'大阪府',
                'Hyogo':'兵庫県',
                'Nara':'奈良県',
                'Wakayama':'和歌山県',
                'Tottori':'鳥取県',
                'Shimane':'島根県',
                'Okayama':'岡山県',
                'Hiroshima':'広島県',
                'Yamaguchi':'山口県',
                'Tokushima':'徳島県',
                'Kagawa':'香川県',
                'Ehime':'愛媛県',
                'Kochi':'高知県',
                'Fukuoka':'福岡県',
                'Saga':'佐賀県',
                'Nagasaki':'長崎県',
                'Kumamoto':'熊本県',
                'Oita':'大分県',
                'Miyazaki':'宮崎県',
                'Kagoshima':'鹿児島県',
                'Okinawa':'沖縄県',
                }

    prefecture = ""
    max_celsius = ""
    min_celsius = ""
    coordinate = ""
    
    if request.method == "POST":
        geo_request_url = 'https://get.geojs.io/v1/ip/geo.json'
        location_data = requests.get(geo_request_url).json()
        location = location_data['region']
        location_num = area_dic[location]
        prefecture = area_prefecture[location]

        geo_request_url = f'https://weather.tsukumijima.net/api/forecast/city/{location_num}'
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
            coordinate = ('セーターや薄めのコートを着ていくといいでしょう')
        elif 10 <= max_temp < 18 and 8 > min_temp:
            coordinate = 'トレンチコートなどの長めのコートを持参するといいいでしょう'
        elif max_temp < 10 and 2 <= min_temp < 10:
            coordinate = '冬物コートやボアブルゾンを着ていくようにしましょう'
        elif max_temp < 10 and 2 > min_temp:
            coordinate = 'ダウンコートを着ていったり手袋やマフラーが必須ですね'
        
    

    context = {
        'region': prefecture,
        'max': max_celsius,
        'min': min_celsius,
        'coodinate': coordinate
    }
    template = loader.get_template('clothes/index.html')
    
    return HttpResponse(template.render(context, request))

