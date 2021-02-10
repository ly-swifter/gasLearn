"""
Django settings for django_project project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see 
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'phs6-bbyma04e6&9dad=(84#umce^hs+lb1st$*ygyc7k#lenx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'rest_framework',
    'gas_learn',
    'album',
    'django_crontab',
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

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    '*'
)

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)

ROOT_URLCONF = 'django_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us" # zh-hans

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "staticfiles"),
]

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [  # 解析request.data
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ]
}

# 定时任务
'''
*    *    *    *    * ：分别表示 分(0-59)、时(0-23)、天(1 - 31)、月(1 - 12) 、周(星期中星期几 (0 - 7) (0 7 均为周天))
crontab范例：
每五分钟执行    */5 * * * *
每小时执行     0 * * * *
每天执行       0 0 * * *
每周一执行       0 0 * * 1
每月执行       0 0 1 * *
每天23点执行   0 23 * * *
'''
CRONJOBS = [
    ('1 * * * *', 'gas_learn.cron.my_cron_job', ' >> /tmp/logs/gas_learn.log'), # 注意：/tmp/logs 目录要手动创建
]

# Celery配置
# from kombu import Exchange, Queue

# # 设置任务接受的类型，默认是{'json'}
# CELERY_ACCEPT_CONTENT = ['application/json']
# # 设置task任务序列列化为json
# CELERY_TASK_SERIALIZER = 'json'
# # 请任务接受后存储时的类型
# CELERY_RESULT_SERIALIZER = 'json'
# # 时间格式化为中国时间
# CELERY_TIMEZONE = 'Asia/Shanghai'
# # 是否使用UTC时间
# CELERY_ENABLE_UTC = False
# # 指定borker为redis 如果指定rabbitmq CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'
# CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
# # 指定存储结果的地方，支持使用rpc、数据库、redis等等，具体可参考文档 # CELERY_RESULT_BACKEND = 'db+mysql://scott:tiger@localhost/foo' # mysql 作为后端数据库
# CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'
# # 设置任务过期时间 默认是一天，为None或0 表示永不过期
# CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24
# # 设置worker并发数，默认是cpu核心数
# # CELERYD_CONCURRENCY = 12
# # 设置每个worker最大任务数
# CELERYD_MAX_TASKS_PER_CHILD = 100
# # 指定任务的位置
# CELERY_IMPORTS = (
#     'gas_learn.task',
# )
# # 使用beat启动Celery定时任务
# # schedule时间的具体设定参考：https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html
# CELERYBEAT_SCHEDULE = {
#     'add-every-10-seconds': {
#         'task': 'gas_learn.task.scheduler_task',
#         'schedule': 10,
#         'args': ('hello', )
#     },
# }
