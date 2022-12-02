from django.db import models
from django.contrib.auth.models import User

# ユーザーアカウントのモデルクラス
class Account(models.Model):

    # ユーザー認証のインスタンス(1vs1関係)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # 追加フィールド
    gender_list = [
        (0, "男性"),
        (1, "女性")
    ]
    age_list = [
        (0, "19歳以下"),
        (1, "20代"),
        (2, "30代"),
        (3, "40代"),
        (4, "50代"),
        (5, "60歳以上")
    ]
    
    user_gender = models.IntegerField(choices=gender_list)
    user_age = models.IntegerField(choices=age_list)

    def __str__(self):
        return self.user.username

class UploadImage(models.Model):
    image = models.ImageField(upload_to='img/')
    temprature = models.IntegerField(default=0)
    image_id = models.IntegerField(default=0)
