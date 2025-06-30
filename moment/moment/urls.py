from components.djangodav.locks import DummyLock
from applications.webdav.resource import MyDBDavResource
from components.djangodav.acls import FullAcl
from applications.webdav.resource import MyDavResource
from applications.webdav.views import AuthenticatedDavView
from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from .api import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls, name='api'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += [
    re_path(r'^api/fsdav(?P<path>.*)$', AuthenticatedDavView.as_view(resource_class=MyDavResource, lock_class=DummyLock,
                                                    acl_class=FullAcl)),
    re_path(r'^api/dbdav(?P<path>.*)$', AuthenticatedDavView.as_view(resource_class=MyDBDavResource,
            lock_class=DummyLock, acl_class=FullAcl)),
]
