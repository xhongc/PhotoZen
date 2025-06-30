def init_task(sender, **kwargs):
    from .models import Album
    Album.objects.get_or_create(name="收藏", owner=None)
    