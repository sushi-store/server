"""
Production Settings for Heroku
"""

import environ
from sushi_store.settings.local import *

env = environ.Env(
    DEBUG=(bool, False)
)

SECRET_KEY = env.str('SECRET_KEY')
FERNET_KEY_EMAIL = bytes(env.str('FERNET_KEY_EMAIL'), 'utf-8')
FERNET_KEY_PASSWORD = bytes(env.str('FERNET_KEY_PASSWORD'), 'utf-8')

CLIENT_URL = env.str('CLIENT_URL')

EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'd3fb44fdb0titt',
        'HOST': 'ec2-52-19-96-181.eu-west-1.compute.amazonaws.com',
        'PORT': '5432',
        'USER': 'mubyatbepwwpfz',
        'PASSWORD': 'd717916ff91f7be4bde555feb24be796dd0d0e5fef955012155bf3bdca6901c9'
    }
}

cloudinary.config(
    cloud_name="sushi-store",
    api_key=env.str('CLOUDINARY_API_KEY'),
    api_secret=env.str('CLOUDINARY_API_SECRET')
)
