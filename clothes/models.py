from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

# ユーザーアカウントのモデルクラス
class Account(models.Model):

    # ユーザー認証のインスタンス
    user = models.OneToOneField(User, on_delete=models.CASCADE)

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

# 画像アップロードのモデルクラス
class UploadImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='img/')
    temperature = models.IntegerField(default=0)
    sum_like = models.IntegerField(default=0)

# 画像に対するいいね
class LikeForPost(models.Model):
    target = models.ForeignKey(UploadImage, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)