from .default import *
#
# # DEBUG = False
# ALLOWED_HOSTS = ["0.0.0.0", "localhost"]
# ALLOWED_HOSTS = ["0.0.0.0", "localhost"]

DATABASES = {
    'default': {
        'PROD_DB_ENGINE': os.environ.setdefault("SECRET_KEY", 'django.db.backends.postgresql')
            ,
        'NAME': os.environ.get("PROD_DB_NAME"),
        'USER': os.environ.get("PROD_DB_USER"),
        'PASSWORD': os.environ.get("PROD_DB_PASSWORD"),
        'HOST': os.environ.get("PROD_DB_HOST"),
        'PORT': os.environ.get("PROD_DB_PORT"),
    }
}
