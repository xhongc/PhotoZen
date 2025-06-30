from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Album(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='albums', null=True, blank=True)
    cover_photo = models.ForeignKey('photos.Photo', on_delete=models.SET_NULL, null=True, blank=True, related_name='album_covers')
    photos = models.ManyToManyField('photos.Photo', related_name='albums', blank=True)

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return self.name

    @property
    def photos_count(self):
        return self.photos.count()
