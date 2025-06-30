from django.apps import AppConfig
from django.db.models.signals import post_migrate,pre_migrate

from applications.album.handlers import init_task


class AlbumConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications.album'

    def ready(self):
        post_migrate.connect(init_task, self)