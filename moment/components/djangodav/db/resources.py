from operator import and_
from functools import reduce
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils.functional import cached_property
from django.utils.timezone import now
from components.djangodav.base.resources import BaseDavResource
from components.djangodav.utils import url_join


class BaseDBDavResource(BaseDavResource):
    collection_model = None
    object_model = None

    collection_attribute = 'parent'
    created_attribute = 'created'
    modified_attribute = 'modified'
    name_attribute = 'name'
    size_attribute = 'size'

    collection_select_related = tuple()
    object_select_related = tuple()

    collection_prefetch_related = tuple()
    object_prefetch_related = tuple()

    def __init__(self, path, **kwargs):
        if 'obj' in kwargs:  # Accepting ready object to reduce db requests
            self.__dict__['obj'] = kwargs.pop('obj')
        super(BaseDBDavResource, self).__init__(path)

    @cached_property
    def obj(self):
        raise NotImplementedError

    @property
    def getcontentlength(self):
        return getattr(self.obj, self.size_attribute)

    def get_created(self):
        if self.is_root:
            return now()
        return getattr(self.obj, self.created_attribute)

    def get_modified(self):
        if self.is_root:
            return now()
        return getattr(self.obj, self.modified_attribute)

    @property
    def is_collection(self):
        return self.is_root or isinstance(self.obj, self.collection_model)

    @property
    def is_object(self):
        return isinstance(self.obj, self.object_model)

    @cached_property
    def exists(self):
        return self.is_root or bool(self.obj)

    def get_model_lookup_kwargs(self, **kwargs):
        return self.get_model_kwargs(**kwargs)

    def get_model_kwargs(self, **kwargs):
        return kwargs

    def get_children(self):
        """Return an iterator of all direct children of this resource."""
        if not self.exists or isinstance(self.obj, self.object_model):
            return

        models = [
            [self.collection_model, self.collection_select_related, self.collection_prefetch_related],
            [self.object_model, self.object_select_related, self.object_prefetch_related]
        ]
        for model, select_related, prefetch_related in models:
            qs = model.objects
            if select_related:
                qs = qs.select_related(*select_related)
            if prefetch_related:
                qs = qs.prefetch_related(*prefetch_related)
            kwargs = self.get_model_lookup_kwargs(**{self.collection_attribute: self.obj})
            for child in qs.filter(**kwargs):
                yield self.clone(
                    url_join(*(self.path + [child.name])),
                    obj=child    # Sending ready object to reduce db requests
                )

    def read(self):
        raise NotImplementedError

    def write(self, content):
        raise NotImplementedError

    def delete(self):
        if not self.obj:
            return
        self.obj.delete()


class NameLookupDBDavMixIn(object):
    """Object lookup by joining collections tables to fit given path"""

    def __init__(self, path, **kwargs):
        self.possible_collection = path.endswith("/")
        super(NameLookupDBDavMixIn, self).__init__(path, **kwargs)

    def get_object(self):
        return self.get_model_by_path('object', self.path)

    def get_collection(self):
        return self.get_model_by_path('collection', self.path)

    def create_collection(self):
        name = self.path[-1]
        parent = self.clone("/".join(self.path[:-1])).obj
        kwargs = self.get_model_kwargs(**{self.collection_attribute: parent, 'name': name})
        self.collection_model.objects.create(**kwargs)

    @cached_property
    def obj(self):
        if not self.path:
            return None

        if self.possible_collection:  # Reducing queries
            attempts = [self.get_collection, self.get_object]
        else:
            attempts = [self.get_object, self.get_collection]

        for get_object in attempts:
            try:
                return get_object()
            except ObjectDoesNotExist:
                continue

    def get_model_by_path(self, model_attr, path):
        if not path:
            return None

        args = []
        i = 0
        for part in reversed(path):
            args.append(Q(**{"__".join(([self.collection_attribute] * i) + [self.name_attribute]): part}))
            i += 1
        qs = getattr(self, "%s_model" % model_attr).objects.filter(**self.get_model_lookup_kwargs())

        select_related = ["__".join([self.collection_attribute] * i) for i in range(1, len(path))]
        select_related += getattr(self, "%s_select_related" % model_attr)
        if select_related:
            qs = qs.select_related(*select_related)

        prefetch_related = getattr(self, "%s_prefetch_related" % model_attr)
        if prefetch_related:
            qs = qs.prefetch_related(*prefetch_related)

        args.append(Q(**{"__".join([self.collection_attribute] * len(path)): None}))
        try:
            return qs.filter(reduce(and_, args))[0]
        except IndexError:
            raise qs.model.DoesNotExist()

    def copy_object(self, destination):
        self.obj.pk = None
        name = destination.path[-1]
        collection = self.clone(destination.get_parent_path()).obj
        setattr(self.obj, self.name_attribute, name)
        setattr(self.obj, self.collection_attribute, collection)
        setattr(self.obj, self.created_attribute, now())
        setattr(self.obj, self.modified_attribute, now())
        self.obj.save(force_insert=True)

    def move_object(self, destination):
        name = destination.path[-1]
        collection = self.clone(destination.get_parent_path()).obj
        setattr(self.obj, self.name_attribute, name)
        setattr(self.obj, self.collection_attribute, collection)
        setattr(self.obj, self.modified_attribute, now())
        self.obj.save(update_fields=[self.name_attribute, self.collection_attribute, self.modified_attribute])
