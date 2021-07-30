"These settings make the tests run significantly faster"""
from config.settings.dev import *  # noqa:F401, F403


PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

CELERY_BROKER_BACKEND = 'memory'
