from django.apps import AppConfig


class EventConfig(AppConfig):
    name = 'eResponse.event'

    def ready(self):
        import eResponse.event.signals
