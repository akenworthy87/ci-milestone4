from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    name = 'checkout'

    def ready(self):
        # '(F401) Imported but unused' linting error is a false positive.
        import checkout.signals
