from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'eResponse.user'

    def ready(self):
        from . import signals
        import eResponse.user.signals
