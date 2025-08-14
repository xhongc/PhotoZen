from django.core.management.base import BaseCommand
from applications.album.models import Album


class Command(BaseCommand):
    help = 'Create system albums (Favorites) if they do not exist'

    def handle(self, *args, **options):
        # Create favorites album if it doesn't exist
        favorite_album, created = Album.objects.get_or_create(
            name='收藏',
            defaults={
                'description': '收藏的照片',
                'owner': None  # System album
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Successfully created "收藏" album')
            )
        else:
            self.stdout.write(
                self.style.WARNING('"收藏" album already exists')
            )