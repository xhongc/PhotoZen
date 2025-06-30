from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

# Create your models here.

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
    taken_time = models.DateTimeField(null=False, blank=False, default=timezone.now)
    size = models.IntegerField()  # File size in bytes
    width = models.IntegerField()
    height = models.IntegerField()
    format = models.CharField(max_length=10)  # e.g., 'JPG', 'PNG'
    
    tags = models.ManyToManyField(Tag, related_name='photos')
    favorited_by = models.ManyToManyField(User, related_name='favorite_photos', blank=True)
    rating = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-upload_time']

    def update_rating(self, new_rating):
        """更新照片的平均评分"""
        ratings = self.ratings.all()
        total_rating = sum(r.rating for r in ratings)
        self.rating = (total_rating + new_rating) / (len(ratings) + 1)
        self.save()

class PhotoRating(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('photo', 'user')
        ordering = ['-created_time']

class Location(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    photos = models.ManyToManyField(Photo, related_name='locations')

    def __str__(self):
        return self.name
