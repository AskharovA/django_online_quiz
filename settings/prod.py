from .base import *

DEBUG = False

ADMINS = [
    ('Akylbek A', 'androidepta@gmail.com')
]

ALLOWED_HOSTS = ["www.playquiz.kz", "playquiz.kz", 'localhost']
CSRF_TRUSTED_ORIGINS = ["www.playquiz.kz", "playquiz.kz"]

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": "db",
        "PORT": 5432,
    }
}

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

REDIS_URL = 'redis://redis:6379'
CHANNEL_LAYERS['default']['CONFIG']['hosts'] = [REDIS_URL]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        # Если вам нужно логирование для приложений
        'config': {  # Замените 'myapp' на имя вашего приложения
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
