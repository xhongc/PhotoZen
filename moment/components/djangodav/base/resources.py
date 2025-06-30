from hashlib import md5
from mimetypes import guess_type

from django.utils.encoding import force_bytes
from urllib.parse import quote
from components.djangodav.utils import rfc3339_date, rfc1123_date, safe_join


class BaseDavResource(object):
    ALL_PROPS = ['getcontentlength', 'creationdate', 'getlastmodified', 'resourcetype', 'displayname']

    LIVE_PROPERTIES = [
        '{DAV:}getetag', '{DAV:}getcontentlength', '{DAV:}creationdate',
        '{DAV:}getlastmodified', '{DAV:}resourcetype', '{DAV:}displayname'
    ]

    def __init__(self, path):
        self.path = []
        path = path.strip("/")
        if path:
            self.path = path.split("/")

    def get_path(self):
        return ("/" if self.path else "") + "/".join(self.path) + ("/" * (self.is_collection))

    def get_escaped_path(self):
        path = [quote(p) for p in self.path]
        return ("/" if path else "") + "/".join(path) + ("/" * self.is_collection)

    @property
    def displayname(self):
        if not self.path:
            return None
        return self.path[-1]

    @property
    def is_root(self):
        return not bool(self.path)

    def get_parent_path(self):
        path = self.path[:-1]
        return "/" + "/".join(path) + "/" if path else ""

    def get_parent(self):
        return self.clone(self.get_parent_path())

    def get_descendants(self, depth=1, include_self=True):
        """Return an iterator of all descendants of this resource."""
        if include_self:
            yield self
        # If depth is less than 0, then it started out as -1.
        # We need to keep recursing until we hit 0, or forever
        # in case of infinity.
        if depth != 0:
            for child in self.get_children():
                for desc in child.get_descendants(depth=depth-1, include_self=True):
                    yield desc

    @property
    def getcontentlength(self):
        raise NotImplementedError()

    @property
    def creationdate(self):
        """Return the create time as rfc3339_date."""
        return rfc3339_date(self.get_created())

    @property
    def getlastmodified(self):
        """Return the modified time as http_date."""
        return rfc1123_date(self.get_modified())

    def get_created(self):
        """Return the create time as datetime object."""
        raise NotImplementedError()

    def get_modified(self):
        """Return the modified time as datetime object."""
        raise NotImplementedError()

    @property
    def getetag(self):
        raise NotImplementedError()

    def copy(self,  destination, depth=-1):
        if self.is_collection:
            if not destination.exists or not destination.is_collection:
                destination.create_collection()
            self.copy_collection(destination, depth)
        else:
            if destination.is_object:
                destination.delete()
            self.copy_object(destination)

    def copy_collection(self, destination, depth=-1):
        """Called to copy a resource to a new location. Overwrite is assumed, the DAV server
        will refuse to copy to an existing resource otherwise. This method needs to gracefully
        handle a pre-existing destination of any type. It also needs to respect the depth
        parameter. depth == -1 is infinity."""
        # If depth is less than 0, then it started out as -1.
        # We need to keep recursing until we hit 0, or forever
        # in case of infinity.
        if depth != 0:
            for child in self.get_children():
                child.copy(self.clone(safe_join(destination.get_path(), child.displayname)),
                           depth=depth-1)

    def copy_object(self, destination):
        raise NotImplemented()

    def move(self,  destination):
        if self.is_collection:
            if not destination.exists or not destination.is_collection:
                destination.create_collection()
            self.move_collection(destination)
        else:
            if destination.is_object:
                destination.delete()
            self.move_object(destination)

    def move_collection(self, destination):
        """Called to move a resource to a new location. Overwrite is assumed, the DAV server
        will refuse to move to an existing resource otherwise. This method needs to gracefully
        handle a pre-existing destination of any type."""
        for child in self.get_children():
            child.move(self.clone(safe_join(destination.get_path(), child.displayname)))
        self.delete()

    def clone(self, *args, **kwargs):
        return self.__class__(*args, **kwargs)

    def move_object(self, destination):
        raise NotImplemented()

    def write(self, content):
        raise NotImplementedError()

    def read(self):
        raise NotImplementedError()

    @property
    def is_collection(self):
        raise NotImplementedError()

    @property
    def content_type(self):
        return guess_type(self.displayname)[0]

    @property
    def is_object(self):
        raise NotImplementedError()

    @property
    def exists(self):
        raise NotImplementedError()

    def get_children(self):
        raise NotImplementedError()

    def delete(self):
        raise NotImplementedError()

    def create_collection(self):
        raise NotImplementedError()


class MetaEtagMixIn(object):
    @property
    def getetag(self):
        """Calculate an etag for this resource. The default implementation uses an md5 sub of the
        absolute path modified time and size. Can be overridden if resources are not stored in a
        file system. The etag is used to detect changes to a resource between HTTP calls. So this
        needs to change if a resource is modified."""
        hashsum = md5()
        hashsum.update(force_bytes(self.displayname))
        hashsum.update(force_bytes(self.creationdate))
        hashsum.update(force_bytes(self.getlastmodified))
        hashsum.update(force_bytes(self.getcontentlength))
        return hashsum.hexdigest()
