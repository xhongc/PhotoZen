from components.djangodav.db.resources import NameLookupDBDavMixIn, BaseDBDavResource
from django.utils.timezone import now
from hashlib import md5
from base64 import b64encode, b64decode
from django.conf import settings
from components.djangodav.base.resources import MetaEtagMixIn
from components.djangodav.fs.resources import DummyFSDAVResource
from applications.webdav.models import CollectionModel, ObjectModel

class MyDavResource(MetaEtagMixIn, DummyFSDAVResource):
    root = settings.MEDIA_ROOT


class MyDBDavResource(NameLookupDBDavMixIn, BaseDBDavResource):
    collection_model = CollectionModel
    object_model = ObjectModel

    def write(self, content):
        size = len(content)
        hashsum = md5(content).hexdigest()
        content = b64encode(content)
        if not self.exists:
            self.object_model.objects.create(
                name=self.displayname,
                parent=self.get_parent().obj,
                md5=hashsum,
                size=size,
                content=content
            )
            return
        self.obj.size = size
        self.obj.modified = now()
        self.obj.content = content
        self.md5 = hashsum
        self.obj.save(update_fields=['content', 'size', 'modified', 'md5'])

    def read(self):
        return b64decode(self.obj.content)

    @property
    def getetag(self):
        return self.obj.md5

    @property
    def getcontentlength(self):
        return self.obj.size
