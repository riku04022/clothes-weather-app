from pathlib import Path
import os

if os.getenv('GAE_APPLICATION', None):
    # 本番環境
    DEBUG = False
    ALLOWED_HOSTS = ['weather-clothes-app.an.r.appspot.com']
else:
    # 開発環境
    DEBUG = True
    ALLOWED_HOSTS = ['*']

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = os.path.join(BASE_DIR,'templates')

# Secret Key
SECRET_KEY = 'django-insecure-*8s1twu^)@hnhur+j8&!qo6u1thht12$=69a_1o5jz1d&3kitt'

# Application definition
INSTALLED_APPS = [
    'clothes.apps.ClothesConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'
LOGIN_URL='/clothes/login'     # ログイン
LOGOUT_URL='/clothes/logout'   # ログアウト
LOGIN_REDIRECT_URL = '/clothes/home'     # ログイン
LOGOUT_REDIRECT_URL='/clothes/login'    # ログアウト


# テンプレート
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
            'libraries': {
                'utility': 'clothes.templatetags.clothes'
            }
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'

# データベース
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
"""
if os.getenv('GAE_APPLICATION', None):
       # GAE本番環境
   DATABASES = {
       'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '/cloudsql/weather-clothes-app:asia-northeast1:cloud-mysql',
        'USER': 'riku04022',
        'PASSWORD': 'Riku0402',
        'NAME': 'USER',
    }
   }
else:
   # 開発環境
   # 事前に./cloud_sql_proxyを実行してプロキシ経由でアクセスできるようにする必要がある。
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '127.0.0.1',
            'PORT': '3306',
            'USER': 'root',
            'PASSWORD': 'root0123',
            'NAME': 'USER',
        }
}



# パスワード有効性
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS':{"min_length":6},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# パスワードのハッシュ化
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.BCryptPasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
]
"""


# Internationalization
LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'clothes/static')

# Media
MEDIA_ROOT = os.path.join(BASE_DIR, 'clothes/media/')
MEDIA_URL = "/media/"

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'