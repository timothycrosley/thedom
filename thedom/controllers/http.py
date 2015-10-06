'''
    HTTP.py

    Basic Classes that work together to define HTTP requests and responses.

    Copyright (C) 2015  Timothy Edmund Crosley

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''

import pprint
import urllib
from collections import namedtuple
from thedom.MultiplePythonSupport import *

try:
    from django.http import HttpResponse as djangoResponse
except ImportError as e:
    djangoResponse = None

try:
    from google.appengine.api import users as appEngineUsers
except ImportError as e:
    appEngineUsers = None


class Cookie(namedtuple('Cookie', ['key', 'value', 'maxAge', 'expires', 'path', 'domain', 'secure', 'httpOnly'])):
    """
        Defines an HTTP cookie object to be used for storing basic data on the client side during a single session.
    """
    __slots__ = ()

    def toHeader(self):
        """
            Converts the cookie data into that expected by the Set-Cookie header.
        """
        value = ["%s=%s" % (self.key, self.value)]

        if self.maxAge:
            value.append("Max-Age=%s" % (self.maxAge, ))
        if self.expires:
            value.append("Expires=%s" % (self.expires, ))
        if self.path:
            value.append("Path=%s" % (self.path, ))
        if self.domain:
            value.append("Domain=%s" % (self.domain, ))
        if self.secure:
            value.append("Secure")
        if self.httpOnly:
            value.append("HttpOnly")

        return ";".join(value)


class FieldDict(dict):
    """
        Adds convenience methods to the basic python dictionary specific to HTTP field dictionaries
    """

    def get(self, field, default=''):
        """
            Overwrites dict behavior to return empty string by default - to be more consistent with browser behavior
        """
        return dict.get(self, field, default)

    def getSet(self, field):
        """
            Returns a set version of a value (independent to it's form in the dictionary)
        """
        field = self.get(field)
        if not field:
            return set([])
        if type(field) != list:
            return set([field])
        else:
            return set(field)

    def getList(self, field):
        """
            Returns a list version of a value (independent to it's form in the dictionary)
        """
        field = self.get(field)
        if not field:
            return []
        if type(field) != list:
            return [field]
        else:
            return field

    def first(self, fieldName, defaultValue=''):
        """
            Returns the first item if the value is a list otherwise returns the whole value
        """
        field = self.get(fieldName, defaultValue)
        if type(field) == list:
            if field:
                return field[0]
            return defaultValue
        return field

    def last(self, fieldName, defaultValue=''):
        """
            Returns the last item if the value is a list otherwise returns the whole value
        """
        field = self.get(fieldName, defaultValue)
        if type(field) == list:
            if field:
                return field[-1]
            return defaultValue
        return field

    def subset(self, fields, default=''):
        """
            Returns a subset of itself based on a list of fields
        """
        fieldDict = self.__class__()
        for field in fields:
            fieldDict[field] = self.get(field, default)

        return fieldDict

    def queryString(self):
        """
            Returns a queryString version of the dictionary - useful for making URL GET requests
        """
        params = []
        for key, value in iteritems(self):
            if type(value) in (list, set, tuple):
                for instance in value:
                    params.append("%s=%s" % (key, urllib.quote(instance)))
            else:
                params.append("%s=%s" % (key, urllib.quote(value)))

        return "&".join(params)


class Response(object):
    """
        Defines the abstract concept of an HTTP response
    """
    __slots__ = ('content', 'status', 'contentType', '_headers', 'cookies', 'scripts', 'charset')

    class Status(object):
        """
            A mapping of all HTTP response codes to their English meaning

            see: http://en.wikipedia.org/wiki/List_of_HTTP_status_codes
        """
        # Informational
        CONTINUE = 100
        SWITCHING_PROTOCOLS = 101
        PROCESSING = 102

        # Success
        OK = 200
        CREATED = 201
        ACCEPTED = 202
        NON_AUTHORITAVE = 203 # Information returned but might may not be owned by server
        NO_CONTENT = 204
        RESET_CONTENT = 205 # The requester made a reset response and it was successful
        PARTIAL_CONTENT = 206
        MULTI_STATUS = 207
        ALREADY_REPORTED = 208

        # Redirection
        MULTIPLE_CHOICES = 300
        MOVED = 301
        FOUND = 302
        SEE_OTHER = 303
        NOT_MODIFIED = 304
        USE_PROXY = 305
        TEMPORARY_REDIRECT = 307
        PERMANENT_REDIRECT = 308

        # Client error
        BAD_REQUEST = 400
        UNAUTHORIZED = 401
        PAYMENT_REQUIRED = 402
        FORBIDDEN = 403
        NOT_FOUND = 404
        NOT_ALLOWED = 405
        NOT_ACCEPTABLE = 406
        PROXY_AUTHENTICATION_REQUIRED = 407
        REQUEST_TIMEOUT = 408
        CONFLICT = 409
        GONE = 410
        LENGTH_REQUIRED = 411
        PRECONDITION_FAILED = 412
        REQUEST_ENTITY_TOO_LARGE = 413
        REQUEST_URI_TOO_LONG = 414
        UNSUPPORTED_MEDIA_TYPE = 415
        REQUESTED_RANGE_NOT_SATISFIABLE = 416
        EXPECTATION_FAILED = 417
        IM_A_TEAPOT = 418
        UNPROCESSABLE_ENTITY = 422
        LOCKED = 423
        FAILED_DEPENDENCY = 424
        METHOD_FAILURE = 424
        UNORDERED_COLLECTION = 425
        UPGRADE_REQUIRED = 426
        PRECONDITION_REQUIRED = 428
        TOO_MANY_REQUESTS = 429
        HEADER_FIELDS_TOO_LARGE = 431
        UNAVAILABLE_FOR_LEGAL_REASONS = 451

        # Server error
        INTERNAL_SERVER_ERROR = 500
        NOT_IMPLEMENTED = 501
        BAD_GATEWAY = 502
        SERVICE_UNAVAILABLE = 503
        GATEWAY_TIMEOUT = 504
        HTTP_VERSION_NOT_SUPPORTED = 505
        CIRCULAR_REFERENCE = 506
        INSUFFICIENT_STORAGE = 507
        INFINITE_LOOP = 508
        BANDWIDTH_LIMIT_EXCEEDED = 509
        NOT_EXTENDED = 510
        NETWORK_AUTHENTICATION_REQUIRED = 511

    class ContentType(object):
        """
            A mapping of common content types used in web applications

            see: http://en.wikipedia.org/wiki/Internet_media_type
        """
        TEXT = "text/plain"
        HTML = "text/html"
        JSON = "application/json"
        CSS = "text/css"
        CSV = "text/csv"
        JAVASCRIPT = "text/javascript"
        VCARD = "text/vcard"
        XML = "text/xml"

    def __init__(self, content='', contentType=None, status=None, charset="UTF-8", isDynamic=True):
        self.content = content
        self.contentType = contentType or self.ContentType.HTML
        self.charset = charset
        self.status = status or self.Status.OK
        self.cookies = FieldDict({})
        self._headers = {}
        self.scripts = None
        if isDynamic: # If content is dynamically generated (and it almost always is) don't let the browser cache
            self['Cache-Control'] = 'no-cache, must-revalidate'
            self['Pragma'] = 'no-cache'
            self['Expires'] = 'Thu, 01 DEC 1994 01:00:00 GMT' # Some time in the past

    def get(self, header, default=None):
        """
            Returns header value if it exists or default
        """
        return self._headers.get(header, default)

    def setCookie(self, key, value='', maxAge=None, expires=None, path='/', domain=None, secure=False,
                    httpOnly=False):
        """
            Sets a cookie
        """
        newCookie = Cookie(key, value, maxAge, expires, path, domain, secure, httpOnly)
        self.cookies[key] = newCookie
        return newCookie

    def __setitem__(self, header, value):
        """
            Implement __setItem__ to support dict like setting of headers right on the request object
        """
        self._headers[header] = value

    def __delitem__(self, header):
        """
            Implement __delItem__ to support dict like deleting of headers right on the request object
        """
        try:
            del self._headers[header]
        except KeyError:
            pass

    def __getitem__(self, header):
        """
            Implement __getItem__ to support dict like deleting of headers on the request object
        """
        return self._headers[header]

    def serialize(self):
        """
            Returns a plain dictionary of the response for serialization purposes.
        """
        return {'responseText':self.content, 'status':self.status, 'contentType':self.contentType}

    def toAppEngineResponse(self, response):
        """
            Passes the contents of this response into the given app engine response object
        """
        response.out.write(self.content)
        response.set_status(self.status)
        response.headers.add('Content-Type', self.contentType + ";charset=" + self.charset)

        for header, value in iteritems(self._headers):
            response.headers.add(header, value)

        for cookie in itervalues(self.cookies):
            response.headers.add('Set-Cookie', cookie.toHeader())
            
    def redirect(self, location):
        self.status = self.Status.TEMPORARY_REDIRECT
        self['Location'] = location
        self.content = ""
        return self

    def toDjangoResponse(self, cls=djangoResponse):
        """
            Converts the given response to the Django HTTPResponse object
            cls - the django HTTPResponse class or compatible object type
        """
        djangoResponse = cls(self.content, self.contentType + ";charset=" + self.charset, self.status)
        for header, value in iteritems(self._headers):
            djangoResponse[header] = value

        for cookie in itervalues(self.cookies):
            djangoResponse.set_cookie(*cookie)

        return djangoResponse


class Request(object):
    """
        Defines the abstract concept of an HTTP request
    """

    def __init__(self, fields=None, body="", cookies=None, meta=None, files=None, path=None, method=None, user=None,
                 native=None, session=None):
        self.fields = FieldDict(fields or {})
        self.body = body
        self.cookies = FieldDict(cookies or {})
        self.meta = FieldDict(meta or {})
        self.files = FieldDict(files or {})
        self.path = path or ""
        self.user = user
        self.native = native
        self.method = method
        self.response = Response()
        self.session = session

    def __unicode__(self):
        return ("PATH:%(path)s\n"
                "METHOD:%(method)s\n"
                "\n"
                "FIELDS:\n"
                "%(fields)s\n\n"
                "COOKIES:\n"
                "%(cookies)s\n\n"
                "META:\n"
                "%(meta)s\n\n"
                "BODY:\n"
                "%(body)s\n\n") % {'path':self.path, 'method':self.method, 'fields':pprint.pformat(self.fields),
                                   'cookies':pprint.pformat(self.cookies), 'meta':pprint.pformat(self.meta),
                                   'body':self.body}

    def __str__(self):
        return unicode(self).encode('utf-8')

    def copy(self):
        """
            Returns a smart copy of the request object
        """
        copy =  self.__class__(fields=self.fields.copy(), body=self.body, cookies=self.cookies.copy(),
                               meta=self.meta.copy(), files=self.files.copy(), path=self.path, method=self.method,
                               user=self.user, native=self.native, session=self.session)
        copy.response.content = self.response.content
        copy.response.status = self.response.status
        copy.response.contentType = self.response.contentType
        copy.response._headers = self.response._headers.copy()
        copy.response.cookies = self.response.cookies.copy()
        copy.response.scripts = self.response.scripts
        copy.response.charset = self.response.charset
        return copy

    def isAjax(self):
        """
            Returns true if the request is explicitly flagged as using an XMLHttpRequest
        """
        return self.meta.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    @classmethod
    def fromAppEngineRequest(cls, appEngineRequest, method="GET", session=None):
        fields = {}
        for name in appEngineRequest.arguments():
            value = appEngineRequest.get_all(name)
            if len(value) == 1:
                value = value[0]
            fields[name] = value

        return cls(fields, appEngineRequest.body, dict(appEngineRequest.cookies), None, None, appEngineRequest.path,
                   method, user=appEngineUsers.get_current_user(), native=appEngineRequest, session=session)



    @classmethod
    def fromDjangoRequest(cls, djangoRequest):
        """
            Creates a new request object from a Django request object
        """
        if djangoRequest.method in ['PUT', 'DELETE']:
            oldMethod = djangoRequest.method
            djangoRequest.method = "POST"
            djangoRequest._load_post_and_files()
            djangoRequest.method = oldMethod
        fields = dict(djangoRequest.POST)
        fields.update(dict(djangoRequest.GET))
        for key, value in iteritems(fields):
            if type(value) in (tuple, list) and len(value) == 1:
                fields[key] = value[0]

        return cls(fields, djangoRequest.body, djangoRequest.COOKIES, djangoRequest.META, djangoRequest.FILES,
                   djangoRequest.path, djangoRequest.method, user=djangoRequest.user, native=djangoRequest)

