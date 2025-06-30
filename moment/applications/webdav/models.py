from django.db import models
from django.utils.timezone import now


class BaseDavModel(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(default=now)
    modified = models.DateTimeField(default=now)

    class Meta:
        abstract = True


class CollectionModel(BaseDavModel):
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    size = 0

    class Meta:
        unique_together = (('parent', 'name'),)


class ObjectModel(BaseDavModel):
    parent = models.ForeignKey(CollectionModel, blank=True, null=True, on_delete=models.CASCADE)
    size = models.IntegerField(default=0)
    content = models.TextField(default=u"")
    md5 = models.CharField(max_length=255)

    class Meta:
        unique_together = (('parent', 'name'),)
