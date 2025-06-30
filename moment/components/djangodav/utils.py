import datetime, time, calendar
from wsgiref.handlers import format_date_time

from django.utils.encoding import force_str
from django.utils.feedgenerator import rfc2822_date

try:
    from email.utils import parsedate_tz
except ImportError:
    from email.Utils import parsedate_tz
import lxml.builder as lb

# Sun, 06 Nov 1994 08:49:37 GMT  ; RFC 822, updated by RFC 1123
FORMAT_RFC_822 = '%a, %d %b %Y %H:%M:%S GMT'
# Sunday, 06-Nov-94 08:49:37 GMT ; RFC 850, obsoleted by RFC 1036
FORMAT_RFC_850 = '%A %d-%b-%y %H:%M:%S GMT'
# Sun Nov  6 08:49:37 1994       ; ANSI C's asctime() format
FORMAT_ASC = '%a %b %d %H:%M:%S %Y'

WEBDAV_NS = "DAV:"

WEBDAV_NSMAP = {'D': WEBDAV_NS}

D = lb.ElementMaker(namespace=WEBDAV_NS, nsmap=WEBDAV_NSMAP)


def get_property_tag_list(res, *names):
    props = []
    for name in names:
        tag = get_property_tag(res, name)
        if tag is None:
            continue
        props.append(tag)
    return props


def get_property_tag(res, name):
    if name == 'resourcetype':
        if res.is_collection:
            return D(name, D.collection)
        return D(name)
    try:
        if hasattr(res, name):
            return D(name, force_str(getattr(res, name)))
    except AttributeError:
        return


def safe_join(root, *paths):
    """The provided os.path.join() does not work as desired. Any path starting with /
    will simply be returned rather than actually being joined with the other elements."""
    if not root.startswith('/'):
        root = '/' + root
    for path in paths:
        while root.endswith('/'):
            root = root[:-1]
        while path.startswith('/'):
            path = path[1:]
        root += '/' + path
    return root


def url_join(base, *paths):
    """Assuming base is the scheme and host (and perhaps path) we will join the remaining
    path elements to it."""
    paths = safe_join(*paths) if paths else ""
    while base.endswith('/'):
        base = base[:-1]
    return base + paths


def ns_split(tag):
    """Splits the namespace and property name from a clark notation property name."""
    if tag.startswith("{") and "}" in tag:
        ns, name = tag.split("}", 1)
        return ns[1:-1], name
    return "", tag


def ns_join(ns, name):
    """Joins a namespace and property name into clark notation."""
    return '{%s:}%s' % (ns, name)


def rfc3339_date(dt):
    if not dt:
        return ''
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')


def rfc1123_date(dt):
    if not dt:
        return ''
    return rfc2822_date(dt)


def parse_time(timestring):
    value = None
    for fmt in (FORMAT_RFC_822, FORMAT_RFC_850, FORMAT_ASC):
        try:
            value = time.strptime(timestring, fmt)
        except ValueError:
            pass
    if value is None:
        try:
            # Sun Nov  6 08:49:37 1994 +0100      ; ANSI C's asctime() format with timezone
            value = parsedate_tz(timestring)
        except ValueError:
            pass
    if value is None:
        return
    return calendar.timegm(value)
