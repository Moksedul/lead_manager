from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'user'

    # for signal function execution
    def ready(self):
        import user.signals
