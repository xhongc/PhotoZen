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

class PhotoMetadata(models.Model):
    """照片自定义元数据字段"""
    FIELD_TYPES = [
        ('text', '文本'),
        ('number', '数字'),
        ('date', '日期'),
        ('boolean', '布尔值'),
        ('json', 'JSON数据'),
    ]
    
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='custom_metadata')
    key = models.CharField(max_length=100, help_text='字段键名')
    name = models.CharField(max_length=200, help_text='字段显示名称')
    value = models.TextField(help_text='字段值')
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES, default='text')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('photo', 'key')
        ordering = ['created_time']
    
    def __str__(self):
        return f"{self.photo.title} - {self.name}"
    
    def get_typed_value(self):
        """根据字段类型返回适当类型的值"""
        import json
        from datetime import datetime
        
        if self.field_type == 'number':
            try:
                return float(self.value)
            except ValueError:
                return 0
        elif self.field_type == 'boolean':
            return self.value.lower() in ('true', '1', 'yes', 'on')
        elif self.field_type == 'date':
            try:
                return datetime.fromisoformat(self.value)
            except ValueError:
                return None
        elif self.field_type == 'json':
            try:
                return json.loads(self.value)
            except json.JSONDecodeError:
                return {}
        else:
            return self.value
