
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ue_#vhs%9793v_cx2yrqa4ehun0_9f!%uhr-se!v@h1yc)+1fz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}







STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]




EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = '10bid.info@gmail.com'
EMAIL_HOST_PASSWORD = 'guyguy11'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
