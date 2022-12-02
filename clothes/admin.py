from django.contrib import admin

from .models import Account
from .models import UploadImage

admin.site.register(Account)
admin.site.register(UploadImage)


