import hashlib
import mimetypes
from sys import getfilesystemencoding
import os
import datetime
import shutil
import urllib

from django.http import HttpResponse
from django.utils.http import http_date

from components.djangodav.base.resources import BaseDavResource
from components.djangodav.responses import ResponseException
from components.djangodav.utils import safe_join, url_join


fs_encoding = getfilesystemencoding()


class BaseFSDavResource(BaseDavResource):
    """Implements an interface to the file system. This can be subclassed to provide
    a virtual file system (like say in MySQL). This default implementation simply uses
    python's os library to do most of the work."""

    root = None

    def get_abs_path(self):
        """Return the absolute path of the resource. Used internally to interface with
        an actual file system. If you override all other methods, this one will not
        be used."""
        return os.path.join(self.root, *self.path)

    @property
    def getcontentlength(self):
        """Return the size of the resource in bytes."""
        return os.path.getsize(self.get_abs_path())

    def get_created(self):
        """Return the create time as datetime object."""
        return datetime.datetime.fromtimestamp(os.stat(self.get_abs_path()).st_ctime)

    def get_modified(self):
        """Return the modified time as datetime object."""
        return datetime.datetime.fromtimestamp(os.stat(self.get_abs_path()).st_mtime)

    @property
    def is_collection(self):
        """Return True if this resource is a directory (collection in WebDAV parlance)."""
        return os.path.isdir(self.get_abs_path())

    @property
    def is_object(self):
        """Return True if this resource is a file (resource in WebDAV parlance)."""
        return os.path.isfile(self.get_abs_path())

    @property
    def exists(self):
        """Return True if this resource exists."""
        return os.path.exists(self.get_abs_path())

    def get_children(self):
        """Return an iterator of all direct children of this resource."""
        if os.path.isdir(self.get_abs_path()):
            for child in os.listdir(self.get_abs_path()):
                try:
                    is_unicode = isinstance(child, unicode)
                except NameError:  # Python 3 fix
                    is_unicode = isinstance(child, str)
                if not is_unicode:
                    child = child.decode(fs_encoding)
                yield self.clone(url_join(*(self.path + [child])))

    def write(self, content):
        raise NotImplementedError

    def read(self):
        raise NotImplementedError

    def delete(self):
        """Delete the resource, recursive is implied."""
        if self.is_collection:
            for child in self.get_children():
                child.delete()
            os.rmdir(self.get_abs_path())
        elif self.is_object:
            os.remove(self.get_abs_path())

    def create_collection(self):
        """Create a directory in the location of this resource."""
        os.mkdir(self.get_abs_path())

    def copy_object(self, destination, depth=0):
        shutil.copy(self.get_abs_path(), destination.get_abs_path())

    def move_object(self, destination):
        os.rename(self.get_abs_path(), destination.get_abs_path())


class DummyReadFSDavResource(BaseFSDavResource):
    def read(self):
        with open(self.get_abs_path(), 'rb') as f:
            return f.read()


class DummyWriteFSDavResource(BaseFSDavResource):
    def write(self, request):
        with open(self.get_abs_path(), 'wb') as dst:
            shutil.copyfileobj(request, dst)


class DummyFSDAVResource(DummyReadFSDavResource, DummyWriteFSDavResource, BaseFSDavResource):
    pass


class SendFileFSDavResource(BaseFSDavResource):
    quote = False

    def read(self):
        response = HttpResponse()
        full_path = self.get_abs_path().encode('utf-8')
        if self.quote:
            full_path = urllib.quote(full_path)
        response['X-SendFile'] = full_path
        response['Content-Type'] = mimetypes.guess_type(self.displayname)
        response['Content-Length'] = self.getcontentlength
        response['Last-Modified'] = http_date(self.getlastmodified)
        response['ETag'] = self.getetag
        raise ResponseException(response)


class RedirectFSDavResource(BaseFSDavResource):
    prefix = "/"

    def read(self):
        response = HttpResponse()
        response['X-Accel-Redirect'] = url_join(self.prefix, self.get_path().encode('utf-8'))
        response['X-Accel-Charset'] = 'utf-8'
        response['Content-Type'] = mimetypes.guess_type(self.displayname)
        response['Content-Length'] = self.getcontentlength
        response['Last-Modified'] = http_date(self.getlastmodified)
        response['ETag'] = self.getetag
        raise ResponseException(response)
