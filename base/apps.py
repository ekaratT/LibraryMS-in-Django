from django.apps import AppConfig
from django.core.signals import request_finished


class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'

    # This is how to connect the signals.py, otherwise member will not be created.
    def ready(self):
        import base.signals
