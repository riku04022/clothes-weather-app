from django import forms
from django.contrib.auth.models import User
from .models import Account
from .models import UploadImage

# 県庁所在地から市町村コード変換するクラス
class PrefectureForm(forms.Form):
    data=[
        ('lat=43.0351&lon=141.2049', '札幌'), 
        ('lat=40.4928&lon=140.4424', '青森'),
        ('lat=39.4213&lon=141.0909', '盛岡'), 
        ('lat=38.1608&lon=140.5219', '仙台'), 
        ('lat=39.4307&lon=140.0609', '秋田'), 
        ('lat=38.1426&lon=140.2148', '山形'), 
        ('lat=37.4500&lon=140.2804', '福島'), 
        ('lat=36.2029&lon=140.2648', '水戸'), 
        ('lat=36.3357&lon=139.5301', '宇都宮'), 
        ('lat=36.2328&lon=139.0339', '前橋'), 
        ('lat=35.5125&lon=139.3856', 'さいたま'), 
        ('lat=35.3617&lon=140.0724', '千葉'),
        ('lat=35.4122&lon=139.4130', '東京'), 
        ('lat=35.2652&lon=139.3833', '横浜'), 
        ('lat=37.5408&lon=139.0125', '新潟'), 
        ('lat=36.4143&lon=137.1241', '富山'), 
        ('lat=36.3540&lon=136.3732', '金沢'), 
        ('lat=36.0355&lon=136.1319', '福井'), 
        ('lat=35.3950&lon=138.3406', '甲府'), 
        ('lat=36.3905&lon=138.1052', '長野'), 
        ('lat=35.2328&lon=136.4320', '岐阜'), 
        ('lat=34.5837&lon=138.2259', '静岡'), 
        ('lat=35.1802&lon=136.9066', '名古屋'), 
        ('lat=34.4349&lon=136.3031', '津'), 
        ('lat=35.0016&lon=135.5206', '大津'), 
        ('lat=35.0117&lon=135.4520', '京都'), 
        ('lat=34.4111&lon=135.3112', '大阪'),
        ('lat=34.4129&lon=135.1059', '神戸'),
        ('lat=34.4107&lon=135.4958', '奈良'), 
        ('lat=34.1334&lon=135.1003', '和歌山'), 
        ('lat=35.3013&lon=134.1418', '鳥取'), 
        ('lat=35.2820&lon=133.0302', '松江'), 
        ('lat=34.3942&lon=133.5606', '岡山'), 
        ('lat=34.2347&lon=132.2734', '広島'), 
        ('lat=34.1109&lon=131.2817', '山口'), 
        ('lat=34.0357&lon=134.3334', '徳島'), 
        ('lat=34.2025&lon=134.2036', '高松'), 
        ('lat=33.5030&lon=132.4558', '松山'), 
        ('lat=33.3335&lon=133.3152','高知'), 
        ('lat=33.3623&lon=130.2505', '福岡'), 
        ('lat=33.1458&lon=130.1756', '佐賀'), 
        ('lat=32.4441&lon=129.5225', '長崎'), 
        ('lat=32.4723&lon=130.4430', '熊本'), 
        ('lat=33.1417&lon=131.3645', '大分'),
        ('lat=31.5440&lon=131.2526', '宮崎'), 
        ('lat=31.3337&lon=130.3329', '鹿児島'), 
        ('lat=26.1245&lon=127.4052', '那覇'), 
    ]
    choice = forms.ChoiceField(initial='lat=35.4122&lon=139.4130', label='地点を選択', choices=data, required=False)
    
# フォームクラス作成
class AccountForm(forms.ModelForm):
    # パスワード入力：非表示対応
    password = forms.CharField(widget=forms.PasswordInput(),label="パスワード")

    class Meta():
        # ユーザー認証
        model = User
        # フィールド指定
        fields = ('username', 'password')
        # フィールド名指定
        labels = {'username':"ユーザー名"}

# アカウント追加クラス
class AddAccountForm(forms.ModelForm):
    class Meta():
        # モデルクラスを指定
        model = Account
        fields = ('user_gender','user_age',)
        labels = {'user_gender':"性別",'user_age':"年齢",}

# 画像アップロードクラス
class UploadForm(forms.ModelForm):
    class Meta():
        model = UploadImage
        fields = ['image']
