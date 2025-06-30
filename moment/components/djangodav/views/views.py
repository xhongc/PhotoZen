import urllib, re
import sys
import json
try:
    import urlparse
except ImportError:
    from urllib import parse as urlparse
from sys import version_info as python_version
from lxml import etree

from django.utils.encoding import force_str
from django.utils.timezone import now
from django.http import HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseBadRequest, \
    HttpResponseNotModified, HttpResponseRedirect, Http404, JsonResponse
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.utils.http import parse_etags
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from components.djangodav.responses import ResponseException, HttpResponsePreconditionFailed, HttpResponseCreated, HttpResponseNoContent, \
    HttpResponseConflict, HttpResponseMediatypeNotSupported, HttpResponseBadGateway, \
    HttpResponseMultiStatus, HttpResponseLocked, HttpResponse
from components.djangodav.utils import WEBDAV_NSMAP, D, url_join, get_property_tag_list, rfc1123_date, parse_time
from components.djangodav import VERSION as djangodav_version
from django import VERSION as django_version, get_version

PATTERN_IF_DELIMITER = re.compile(r'(<([^>]+)>)|(\(([^\)]+)\))')

class DavView(View):
    resource_class = None
    lock_class = None
    acl_class = None
    template_name = 'djangodav/index.html'
    http_method_names = ['options', 'put', 'mkcol', 'head', 'get', 'delete', 'propfind', 'proppatch', 'copy', 'move', 'lock', 'unlock']
    server_header = 'DjangoDav/%s Django/%s Python/%s' % (
        get_version(djangodav_version),
        get_version(django_version),
        get_version(python_version)
    )
    xml_pretty_print = False
    xml_encoding = 'utf-8'

    def no_access(self):
        return HttpResponseForbidden()

    @method_decorator(csrf_exempt)
    def dispatch(self, request, path, *args, **kwargs):
        if path:
            self.path = path
            self.base_url = request.META['PATH_INFO'][:-len(self.path)]
        else:
            self.path = '/'
            self.base_url = request.META['PATH_INFO']

        meta = request.META.get
        self.xbody = kwargs['xbody'] = None
        if (request.method.lower() != 'put'
            and "/xml" in meta('CONTENT_TYPE', '')
            and meta('CONTENT_LENGTH', 0) != ''
            and int(meta('CONTENT_LENGTH', 0)) > 0):
            self.xbody = kwargs['xbody'] = etree.XPathDocumentEvaluator(
                etree.parse(request, etree.XMLParser(ns_clean=True)),
                namespaces=WEBDAV_NSMAP
            )

        if request.method.upper() in self._allowed_methods():
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        try:
            resp = handler(request, self.path, *args, **kwargs)
        except ResponseException as e:
            resp = e.response
        if not 'Allow' in resp:
            methods = self._allowed_methods()
            if methods:
                resp['Allow'] = ", ".join(methods)
        if not 'Date' in resp:
            resp['Date'] = rfc1123_date(now())
        if self.server_header:
            resp['Server'] = self.server_header
        return resp

    def options(self, request, path, *args, **kwargs):
        if not self.has_access(self.resource, 'read'):
            return self.no_access()
        response = self.build_xml_response()
        response['DAV'] = '1,2'
        response['Content-Length'] = '0'
        if self.path in ('/', '*'):
            return response
        response['Allow'] = ", ".join(self._allowed_methods())
        if self.resource.exists and self.resource.is_object:
            response['Allow-Ranges'] = 'bytes'
        return response

    def _allowed_methods(self):
        allowed = [
            'HEAD', 'OPTIONS', 'PROPFIND', 'LOCK', 'UNLOCK',
            'GET', 'DELETE', 'PROPPATCH', 'COPY', 'MOVE', 'PUT', 'MKCOL',
        ]

        return allowed

    def get_access(self, resource):
        """Return permission as DavAcl object. A DavACL should have the following attributes:
        read, write, delete, create, relocate, list. By default we implement a read-only
        system."""
        return self.acl_class(read=True, full=False)

    def has_access(self, resource, method):
        return getattr(self.get_access(resource), method)

    def get_resource_kwargs(self, **kwargs):
        return kwargs

    @cached_property
    def resource(self):
        return self.get_resource(path=self.path)

    def get_resource(self, **kwargs):
        return self.resource_class(**self.get_resource_kwargs(**kwargs))

    def get_depth(self, default='1'):
        depth = str(self.request.META.get('HTTP_DEPTH', default)).lower()
        if not depth in ('0', '1', 'infinity'):
            raise ResponseException(HttpResponseBadRequest('Invalid depth header value %s' % depth))
        if depth == 'infinity':
            depth = -1
        else:
            depth = int(depth)
        return depth

    def evaluate_conditions(self, res):
        if not res.exists:
            return
        etag = res.get_etag()
        mtime = res.get_mtime_stamp()
        cond_if_match = self.request.META.get('HTTP_IF_MATCH', None)
        if cond_if_match:
            etags = parse_etags(cond_if_match)
            if '*' in etags or etag in etags:
                raise ResponseException(HttpResponsePreconditionFailed())
        cond_if_modified_since = self.request.META.get('HTTP_IF_MODIFIED_SINCE', False)
        if cond_if_modified_since:
            # Parse and evaluate, but don't raise anything just yet...
            # This might be ignored based on If-None-Match evaluation.
            cond_if_modified_since = parse_time(cond_if_modified_since)
            if cond_if_modified_since and cond_if_modified_since > mtime:
                cond_if_modified_since = True
            else:
                cond_if_modified_since = False
        cond_if_none_match = self.request.META.get('HTTP_IF_NONE_MATCH', None)
        if cond_if_none_match:
            etags = parse_etags(cond_if_none_match)
            if '*' in etags or etag in etags:
                if self.request.method in ('GET', 'HEAD'):
                    raise ResponseException(HttpResponseNotModified())
                raise ResponseException(HttpResponsePreconditionFailed())
            # Ignore If-Modified-Since header...
            cond_if_modified_since = False
        cond_if_unmodified_since = self.request.META.get('HTTP_IF_UNMODIFIED_SINCE', None)
        if cond_if_unmodified_since:
            cond_if_unmodified_since = parse_time(cond_if_unmodified_since)
            if cond_if_unmodified_since and cond_if_unmodified_since <= mtime:
                raise ResponseException(HttpResponsePreconditionFailed())
        if cond_if_modified_since:
            # This previously evaluated True and is not being ignored...
            raise ResponseException(HttpResponseNotModified())
        # TODO: complete If header handling...
        cond_if = self.request.META.get('HTTP_IF', None)
        if cond_if:
            if not cond_if.startswith('<'):
                cond_if = '<*>' + cond_if
            #for (tmpurl, url, tmpcontent, content) in PATTERN_IF_DELIMITER.findall(cond_if):

    def get(self, request, path, head=False, *args, **kwargs):
        if not self.resource.exists:
            raise Http404("Resource doesn't exists")
        if not path.endswith("/") and self.resource.is_collection:
            return HttpResponseRedirect(request.build_absolute_uri() + "/")
        if path.endswith("/") and self.resource.is_object:
            return HttpResponseRedirect(request.build_absolute_uri().rstrip("/"))
        
        # 检查是否请求JSON格式
        accept_header = request.META.get('HTTP_ACCEPT', '')
        is_json_request = 'application/json' in accept_header
        
        if not self.has_access(self.resource, 'read'):
            return self.no_access()
        
        if is_json_request:
            # 返回JSON格式
            if self.resource.is_object:
                data = {
                    'name': self.resource.displayname,
                    'content_type': self.resource.content_type,
                    'etag': self.resource.getetag,
                    'last_modified': self.resource.getlastmodified,
                    'size': self.resource.getcontentlength
                }
                if not head:
                    data['content'] = self.resource.read().decode('utf-8', errors='ignore')
                return JsonResponse(data)
            else:
                # 集合的JSON表示
                children = []
                for child in self.resource.get_children():
                    children.append({
                        'name': child.displayname,
                        'is_collection': child.is_collection,
                        'path': child.get_path(),
                        'last_modified': child.getlastmodified,
                        'type': 'file' if child.is_object else 'directory'
                    })
                return JsonResponse({
                    'name': self.resource.displayname,
                    'path': self.resource.get_path(),
                    'children': children
                })
        else:
            # 原始HTML/内容响应
            response = HttpResponse()
            if head:
                response['Content-Length'] = 0
            if self.resource.is_object:
                response['Content-Type'] = self.resource.content_type
                response['ETag'] = self.resource.getetag
                if not head:
                    response['Content-Length'] = self.resource.getcontentlength
                    response.content = self.resource.read()
            elif not head:
                response = render(request, self.template_name, dict(resource=self.resource, base_url=self.base_url))
            response['Last-Modified'] = self.resource.getlastmodified
            return response

    def head(self, request, path, *args, **kwargs):
        return self.get(request, path, head=True, *args, **kwargs)

    def put(self, request, path, *args, **kwargs):
        parent = self.resource.get_parent()
        if not parent.exists:
            return HttpResponseConflict("Resource doesn't exists")
        if self.resource.is_collection:
            return HttpResponseNotAllowed(list(set(self._allowed_methods()) - set(['MKCOL', 'PUT'])))
        if not self.resource.exists and not self.has_access(parent, 'write'):
            return self.no_access()
        if self.resource.exists and not self.has_access(self.resource, 'write'):
            return self.no_access()
        created = not self.resource.exists
        self.resource.write(request)
        if created:
            self.__dict__['resource'] = self.get_resource(path=self.resource.get_path())
            return HttpResponseCreated()
        else:
            return HttpResponseNoContent()

    def delete(self, request, path, *args, **kwargs):
        if not self.resource.exists:
            raise Http404("Resource doesn't exists")
        if not self.has_access(self.resource, 'delete'):
            return self.no_access()
        self.lock_class(self.resource).del_locks()
        self.resource.delete()
        response = HttpResponseNoContent()
        self.__dict__['resource'] = self.get_resource(path=self.resource.get_path())
        return response

    def mkcol(self, request, path, *args, **kwargs):
        if self.resource.exists:
            return HttpResponseNotAllowed(list(set(self._allowed_methods()) - set(['MKCOL', 'PUT'])))
        if not self.resource.get_parent().exists:
            return HttpResponseConflict()
        length = request.META.get('CONTENT_LENGTH', 0)
        if length and int(length) != 0:
            return HttpResponseMediatypeNotSupported()
        if not self.has_access(self.resource, 'write'):
            return self.no_access()
        self.resource.create_collection()
        self.__dict__['resource'] = self.get_resource(path=self.resource.get_path())
        return HttpResponseCreated()

    def relocate(self, request, path, method, *args, **kwargs):
        if not self.resource.exists:
            raise Http404("Resource doesn't exists")
        if not self.has_access(self.resource, 'read'):
            return self.no_access()
        # dst = urlparse.unquote(request.META.get('HTTP_DESTINATION', '')).decode(self.xml_encoding)
        if sys.version_info < (3, 0, 0): #py2
            # in Python 2, urlparse requires bytestrings
            dst = urlparse.unquote(request.META.get('HTTP_DESTINATION', '')).decode(self.xml_encoding)
        else:
            # in Python 3, urlparse understands string
            dst = urlparse.unquote(request.META.get('HTTP_DESTINATION', ''))
        if not dst:
            return HttpResponseBadRequest('Destination header missing.')
        dparts = urlparse.urlparse(dst)
        sparts = urlparse.urlparse(request.build_absolute_uri())
        if sparts.scheme != dparts.scheme or sparts.netloc != dparts.netloc:
            return HttpResponseBadGateway('Source and destination must have the same scheme and host.')
        # adjust path for our base url:
        dst = self.get_resource(path=dparts.path[len(self.base_url):])
        if not dst.get_parent().exists:
            return HttpResponseConflict()
        if not self.has_access(self.resource, 'write'):
            return self.no_access()
        overwrite = request.META.get('HTTP_OVERWRITE', 'T')
        if overwrite not in ('T', 'F'):
            return HttpResponseBadRequest('Overwrite header must be T or F.')
        overwrite = (overwrite == 'T')
        if not overwrite and dst.exists:
            return HttpResponsePreconditionFailed('Destination exists and overwrite False.')
        dst_exists = dst.exists
        if dst_exists:
            self.lock_class(self.resource).del_locks()
            self.lock_class(dst).del_locks()
            dst.delete()
        errors = getattr(self.resource, method)(dst, *args, **kwargs)
        if errors:
            return self.build_xml_response(response_class=HttpResponseMultiStatus) # WAT?
        if dst_exists:
            return HttpResponseNoContent()
        return HttpResponseCreated()

    def copy(self, request, path, xbody):
        depth = self.get_depth()
        if depth != -1:
            return HttpResponseBadRequest()
        return self.relocate(request, path, 'copy', depth=depth)

    def move(self, request, path, xbody):
        if not self.has_access(self.resource, 'delete'):
            return self.no_access()
        return self.relocate(request, path, 'move')

    def lock(self, request, path, xbody=None, *args, **kwargs):
        # TODO Lock refreshing
        if not self.has_access(self.resource, 'write'):
            return self.no_access()

        if not xbody:
            return HttpResponseBadRequest('Lockinfo required')

        try:
            depth = int(request.META.get('HTTP_DEPTH', '0'))
        except ValueError:
            return HttpResponseBadRequest('Wrong depth')

        try:
            timeout = int(request.META.get('HTTP_LOCK_TIMEOUT', 'Seconds-600')[len('Seconds-'):])
        except ValueError:
            return HttpResponseBadRequest('Wrong timeout')

        owner = None
        try:
            owner_obj = xbody('/D:lockinfo/D:owner')[0]  # TODO: WEBDAV_NS
        except IndexError:
            owner_obj = None
        else:
            if owner_obj.text:
                owner = owner_obj.text
            if len(owner_obj):
                owner = owner_obj[0].text

        try:
            lockscope_obj = xbody('/D:lockinfo/D:lockscope/*')[0] # TODO: WEBDAV_NS
        except IndexError:
            return HttpResponseBadRequest('Lock scope required')
        else:
            lockscope = lockscope_obj.xpath('local-name()')

        try:
            locktype_obj = xbody('/D:lockinfo/D:locktype/*')[0] # TODO: WEBDAV_NS
        except IndexError:
            return HttpResponseBadRequest('Lock type required')
        else:
            locktype = locktype_obj.xpath('local-name()')

        token = self.lock_class(self.resource).acquire(lockscope, locktype, depth, timeout, owner)
        if not token:
            return HttpResponseLocked('Already locked')

        body = D.activelock(*([
            D.locktype(locktype_obj),
            D.lockscope(lockscope_obj),
            D.depth(force_str(depth)),
            D.timeout("Second-%s" % timeout),
            D.locktoken(D.href('opaquelocktoken:%s' % token))]
            + ([owner_obj] if owner_obj is not None else [])
        ))

        return self.build_xml_response(body)

    def unlock(self, request, path, xbody=None, *args, **kwargss):
        if not self.has_access(self.resource, 'write'):
            return self.no_access()

        token = request.META.get('HTTP_LOCK_TOKEN')
        if not token:
            return HttpResponseBadRequest('Lock token required')
        if not self.lock_class(self.resource).release(token):
            return self.no_access()
        return HttpResponseNoContent()

    def propfind(self, request, path, xbody=None, *args, **kwargs):
        if not self.has_access(self.resource, 'read'):
            return self.no_access()

        if not self.resource.exists:
            raise Http404("Resource doesn't exists")

        if not self.get_access(self.resource):
            return self.no_access()

        get_all_props, get_prop, get_prop_names = True, False, False
        if xbody:
            get_prop = [p.xpath('local-name()') for p in xbody('/D:propfind/D:prop/*')]
            get_all_props = xbody('/D:propfind/D:allprop')
            get_prop_names = xbody('/D:propfind/D:propname')
            if int(bool(get_prop)) + int(bool(get_all_props)) + int(bool(get_prop_names)) != 1:
                return HttpResponseBadRequest()

        children = self.resource.get_descendants(depth=self.get_depth())

        if get_prop_names:
            responses = [
                D.response(
                    D.href(url_join(self.base_url, child.get_escaped_path())),
                    D.propstat(
                        D.prop(*[
                            D(name) for name in child.ALL_PROPS
                        ]),
                        D.status('HTTP/1.1 200 OK'),
                    ),
                )
                for child in children
            ]
        else:
            responses = [
                D.response(
                    D.href(url_join(self.base_url, child.get_escaped_path())),
                    D.propstat(
                        D.prop(
                            *get_property_tag_list(child, *(get_prop if get_prop else child.ALL_PROPS))
                        ),
                        D.status('HTTP/1.1 200 OK'),
                    ),
                )
                for child in children
            ]

        body = D.multistatus(*responses)
        return self.build_xml_response(body, HttpResponseMultiStatus)

    def proppatch(self, request, path, xbody, *args, **kwargs):
        if not self.resource.exists:
            raise Http404("Resource doesn't exists")
        if not self.has_access(self.resource, 'write'):
            return self.no_access()
        depth = self.get_depth(default="0")
        if depth != 0:
            return HttpResponseBadRequest('Invalid depth header value %s' % depth)
        props = xbody('/D:propertyupdate/D:set/D:prop/*')
        body = D.multistatus(
            D.response(
                D.href(url_join(self.base_url, self.resource.get_escaped_path())),
                *[D.propstat(
                    D.status('HTTP/1.1 200 OK'),
                    D.prop(el.tag)
                ) for el in props]
            )
        )
        return self.build_xml_response(body, HttpResponseMultiStatus)

    def build_xml_response(self, tree=None, response_class=HttpResponse, **kwargs):
        # 检查请求的 Accept 头
        accept_header = self.request.META.get('HTTP_ACCEPT', '')
        if 'application/json' in accept_header and 'text/xml' not in accept_header:
            # 如果请求接受 JSON 格式
            if tree is not None:
                # 将 XML 树转换为 JSON
                def xml_to_dict(element):
                    result = {}
                    for child in element:
                        if len(child) == 0:
                            result[child.tag] = child.text
                        else:
                            result[child.tag] = xml_to_dict(child)
                    return result
                
                json_data = xml_to_dict(tree)
                content = json.dumps(json_data, ensure_ascii=False)
                return response_class(
                    content,
                    content_type='application/json; charset="%s"' % self.xml_encoding,
                    **kwargs
                )
            else:
                return response_class(
                    '{}',
                    content_type='application/json; charset="%s"' % self.xml_encoding,
                    **kwargs
                )
        
        # 默认返回 XML 格式
        if tree is not None:
            content = etree.tostring(
                tree,
                xml_declaration=True,
                pretty_print=self.xml_pretty_print,
                encoding=self.xml_encoding
            )
        else:
            content = b''
        return response_class(
            content,
            content_type='text/xml; charset="%s"' % self.xml_encoding,
            **kwargs
        )
