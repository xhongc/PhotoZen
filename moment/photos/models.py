from django.db import models
from django.utils import timezone

# Create your models here.

class Album(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_time = models.DateTimeField(default=timezone.now)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Photo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file_path = models.ImageField(upload_to='photos/%Y/%m/%d/')
    thumbnail_path = models.ImageField(upload_to='thumbnails/%Y/%m/%d/', blank=True)
    upload_time = models.DateTimeField(default=timezone.now)
    taken_time = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField()  # File size in bytes
    width = models.IntegerField()
    height = models.IntegerField()
    format = models.CharField(max_length=10)  # e.g., 'JPG', 'PNG'
    
    albums = models.ManyToManyField(Album, related_name='photos')
    tags = models.ManyToManyField(Tag, related_name='photos')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-upload_time']
