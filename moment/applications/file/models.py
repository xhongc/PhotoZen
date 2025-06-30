from django.db import models

# Create your models here.
class RecycleItem(models.Model):
    path = models.CharField(max_length=255)
    original_path = models.CharField(max_length=255)
    size = models.IntegerField()
    delete_time = models.DateTimeField(auto_now_add=True)
    remaining_days = models.IntegerField()
