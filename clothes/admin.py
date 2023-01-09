from django.contrib import admin
from .models import Account, UploadImage, LikeForPost

# アカウント用データベースコラム
admin.site.register(Account)
# アップロード画像用データベースコラム
admin.site.register(UploadImage)
# いいね用データベースコラム
admin.site.register(LikeForPost)


