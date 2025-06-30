class DavAcl(object):
    """Represents all the permissions that a user might have on a resource. This
    makes it easy to implement virtual permissions."""
    def __init__(self, read=False, write=False, delete=False, full=None):
        if full is not None:
            self.read = self.write = self.delete = \
                self.create = self.relocate = full
        self.read = read
        self.write = write
        self.delete = delete


class ReadOnlyAcl(DavAcl):
    def __init__(self, read=True, write=False, delete=False, full=None):
        super(ReadOnlyAcl, self).__init__(read, write, delete, full)


class FullAcl(DavAcl):
    def __init__(self, read=True, write=True, delete=True, full=None):
        super(FullAcl, self).__init__(read, write, delete, full)
