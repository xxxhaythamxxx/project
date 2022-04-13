from django.apps import AppConfig
from flask_sqlalchemy import SQLAlchemy


class SpareappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'spareapp'
