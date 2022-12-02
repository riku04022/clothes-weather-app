from django import forms
from django.contrib.auth.models import User
from .models import Account
from .models import UploadImage

class PrefectureForm(forms.Form):
    data=[
        ('016010', '札幌'), 
        ('020010', '青森'), 
        ('030010', '盛岡'), 
        ('040010', '仙台'), 
        ('050010', '秋田'), 
        ('060010', '山形'), 
        ('070010', '福島'), 
        ('080010', '水戸'), 
        ('090010', '宇都宮'), 
        ('100010', '前橋'), 
        ('110010', 'さいたま'), 
        ('120010', '千葉'),
        ('130010', '東京'), 
        ('140010', '横浜'), 
        ('150010', '新潟'), 
        ('160010', '富山'), 
        ('170010', '金沢'), 
        ('180010', '福井'), 
        ('190010', '甲府'), 
        ('200010', '長野'), 
        ('210010', '岐阜'), 
        ('220010', '静岡'), 
        ('230010', '名古屋'), 
        ('240010', '津'), 
        ('250010', '大津'), 
        ('260010', '京都'), 
        ('270000', '大阪'),
        ('280010', '神戸'),
        ('290010', '奈良'), 
        ('300010', '和歌山'), 
        ('310010', '鳥取'), 
        ('320010', '松江'), 
        ('330010', '岡山'), 
        ('340010', '広島'), 
        ('350010', '山口'), 
        ('360010', '徳島'), 
        ('370000', '高松'), 
        ('380010', '松山'), 
        ('390010','高知'), 
        ('400010', '福岡'), 
        ('410010', '佐賀'), 
        ('420010', '長崎'), 
        ('430010', '熊本'), 
        ('440010', '大分'),
        ('450010', '宮崎'), 
        ('460010', '鹿児島'), 
        ('471010', '那覇'), 
    ]
    choice = forms.ChoiceField(label='現在地', choices=data, required=False)
    
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

class AddAccountForm(forms.ModelForm):
    class Meta():
        # モデルクラスを指定
        model = Account
        fields = ('user_gender','user_age',)
        labels = {'user_gender':"性別",'user_age':"年齢",}

class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadImage
        fields = ['image']
