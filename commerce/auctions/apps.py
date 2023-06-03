from django.apps import AppConfig
from django.db.models import BigAutoField

class AuctionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auctions'