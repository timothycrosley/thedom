'''
    RequestHandler.py

    Defines the most basic concept of a request handler (an object that accepts a request and returns a response)

    Copyright (C) 2013  Timothy Edmund Crosley

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

import traceback
import types
import json

from . import HTTP
from thedom.MultiplePythonSupport import *

CACHE = {}

class RequestHandler(object):
    """
        Defines the base request handler that supports responding itself or allowing one of its child classes to
        respond
    """
    grabFields = () # fields not part of this controller which will be passed in when this controller is requested
    grabForms = () # forms not part of this controller which will be passed in when this controller is requested
    sharedFields = ()  # fields that are part of this controller & will be passed into all childHandlers
    sharedForms = () # forms that are part of this controller  & will be passed into all childHandlers
    resourceFiles = () # defines the resource files that must be loaded with this control

    def __init__(self, parentHandler=None, initScripts=None, instanceOf=None):
        if instanceOf:
            self.parentHandler = instanceOf.parentHandler
            self.baseName = instanceOf.baseName
            self.accessor = instanceOf.accessor
            self.childHandlers = instanceOf.childHandlers
            self.rootHandler = instanceOf.rootHandler
            for name, handler in iteritems(self.childHandlers):
                if handler != instanceOf:
                    setattr(self, name, handler)
            return
            
        self.parentHandler = parentHandler
        self.baseName = self.__class__.__name__[0].lower() + self.__class__.__name__[1:]
        self.accessor = self.baseName
        self.childHandlers = {}
        if initScripts is None:
            initScripts = []
            
        self.initScripts = initScripts
        self.rootHandler = None

        self._setupDynamicFields()
        grabFields = self.grabFields
        grabForms = self.grabForms
        if parentHandler:
            self.accessor = self.parentHandler.accessor + "-" + self.accessor
            self.grabFields = set(self.grabFields).union(parentHandler.sharedFields)
            self.grabForms = set(self.grabForms).union(parentHandler.sharedForms)
            self.sharedFields = set(self.sharedFields).union(parentHandler.sharedFields)
            self.sharedForms = set(self.sharedFields).union(parentHandler.sharedFields)

        if self.grabFields or self.grabForms:
            self.initScripts.append("DynamicForm.handlers['%s'] = {'grabFields':%s, 'grabForms':%s};" %
                                    (self.accessor, json.dumps(list(self.grabFields)),
                                     json.dumps(list(self.grabForms))))
        self.makeConnections()
        self._registerChildren()

        if not parentHandler:
            for handler in self.allHandlers():
                handler.rootHandler = self
                if handler != self:
                    self.resourceFiles += handler.resourceFiles

            for handler in self.childHandlers.values():
                for name, value in iteritems(self.childHandlers):
                    if value != handler:
                        setattr(handler, name, value)

    def __str__(self):
        return " ".join([string[0].upper() + string[1:] for string in self.accessor.split("-")])

    def _setupDynamicFields(self):
        pass

    def _registerAttribute(self, attributeName, attribute):
        if type(attribute) == type and \
            issubclass(attribute, RequestHandler) and not attribute.__name__.startswith("Abstract"):
            self.registerControl(attribute)
            return True
    
    def _registerChildren(self):
        for attribute, attributeName in ((attribute, getattr(self, attribute, None)) for attribute in dir(self)
                                         if attribute not in ('__class__',)):
            self._registerAttribute(attribute, attributeName)
        
        # Connect sibling handlers so they can communicate with each-other easily
        for childHandlerName, childHandler in self.childHandlers.iteritems():
            for siblingName, siblingHandler in self.childHandlers.iteritems():
                if childHandlerName == siblingName:
                    continue

                childHandler.__setattr__(siblingHandler.baseName, siblingHandler)
            childHandler._postConnections()

    def _postConnections(self):
        pass

    def registerControl(self, controlClass):
        """
            Registers a control, returning the registered instance
        """
        instance = controlClass(parentHandler=self, initScripts=self.initScripts)
        self.childHandlers[instance.baseName] = instance
        self.__setattr__(instance.baseName, instance)
        return instance

    def up(self, levels=1):
        """
            Travels up the request handler tree the requested number of levels
            (equivalent to doing .parentHandler for each level)
        """
        handler = self
        for level in xrange(levels):
            handler = handler.parentHandler
        return handler

    @classmethod
    def djangoView(cls):
        """
            Creates a django view form the request handler object
        """
        return cls().handleDjangoRequest

    def handleDjangoRequest(self, request):
        """
            Handles a django request - returning a django response
        """
        return self.handleRequest(HTTP.Request.fromDjangoRequest(request)).toDjangoResponse()

    def handleRequest(self, request, handlers=None):
        """
            handles a single request returning a response object
        """
        if not handlers:
            handlers = request.fields.get('requestHandler', '')
            if type(handlers) in (list, set, tuple):
                result = [self.handleRequest(request.copy(), handler.split("-")).serialize() for handler in handlers]
                request.response.status = HTTP.Response.Status.MULTI_STATUS
                request.response.contentType = HTTP.Response.ContentType.JSON
                request.response.content = json.dumps(result)
                return request.response

            handlers = handlers.split("-")

        if not handlers.pop(0) in (self.baseName, ""): # Ensure the handler is either the current handler or not spec.
            request.response.status = HTTP.Response.Status.NOT_FOUND
            request.response.content = self.renderNotFound(request, request.fields.get('requestHandler', ''))
        elif handlers:
            handler = self.childHandlers.get(handlers[0], None)
            if not handler:
                request.response.status = HTTP.Response.Status.NOT_FOUND
                request.response.content = self.renderNotFound(request, request.fields.get('requestHandler', ''))
            return handler.handleRequest(request, handlers)
        else:
            try:
                if not self.canView(request) or (request.method != "GET" and not self.canEdit(request)):
                    request.response.status = HTTP.Response.Status.UNAUTHORIZED
                    request.response.content = self.renderUnauthorized(request)

                request.response.content = self.rendered(request)
                    
            except Exception as e:
                request.response.status = HTTP.Response.Status.INTERNAL_SERVER_ERROR
                request.response.content = self.renderInternalError(request, e)

        return request.response

    def cacheKey(self, request):
        """
            If you want a control to auto-cache simply override this method and return a unique hash-able key,
            if not return False.
        """
        return False
    
    def _toCache(self, key, value):
        CACHE[key] = value
        return value
        
    def _fromCache(self, key):
        return CACHE.get(key, "")

    def canView(self, request):
        """
            Returns true if the request's user is allowed to view this content
        """
        if self.parentHandler:
            return self.parentHandler.canView(request)
        else:
            return self._canView(request)

    def _canView(self, request):
        """
            This method should be overwritten to specify if this control is viewable
        """
        return True


    def canEdit(self, request):
        """
            Returns true if the request's user is allowed to edit this content
        """
        if self.parentHandler:
            return self.parentHandler.canEdit(request)
        if not self.canView(request):
            return False

        return self._canEdit(request)

    def _canEdit(self, request):
        """
            This method should be overwritten to specify if this control is editable
        """
        return True

    def allHandlers(self, handlerList=None):
        """
            Returns itself and all child handlers
        """
        if handlerList is None:
            handlerList = []

        handlerList.append(self)
        for child in self.childHandlers.values():
            child.allHandlers(handlerList)
        return handlerList

    def makeConnections(self):
        """
            A safe post instantiation place to make connections between child handlers
        """
        pass

    def rendered(self, request):
        """
            Returns a rendered request handler, either from the cache or by directly calling renderResponse.
            
            Generally should not be overridden
        """
        cacheKey = self.cacheKey(request)
        request.cacheKey = cacheKey
        if not cacheKey:
            return self.renderResponse(request)
        
        rendered = self._fromCache(cacheKey)
        if rendered:
            return rendered
        
        return self._toCache(cacheKey, self.renderResponse(request))
        
    def renderResponse(self, request):
        """
            Defines the response given by the handler (should be overridden by concrete handlers)
        """
        return ""

    def renderNotFound(self, request, resource):
        """
            Defines the response given when a handler is not found. If not defined will look up the parentHandler
            tree till it finds a definition. If it is never overridden will return the plain text error.
        """
        if self.parentHandler:
            return self.parentHandler.renderNotFound(request, exception)

        return "Error: %s was not found." % resource

    def renderInternalError(self, request, exception, handler=None):
        """
            Defines the response given when a handler throws an exception. If not defined will look up the parentHandler
            tree till it finds a definition. If it is never overridden will return the plain text error.
        """
        if handler is None:
            handler = self

        if self.parentHandler:
            return self.parentHandler.renderInternalError(request, exception, handler)
        
        return "Internal Server Error: %s\n%s" % (str(exception), str(traceback.format_exc()))
        

    def renderUnauthorized(self, request):
        """
            Defines the response given when a handler is not authorized. If not defined will look up the parentHandler
            tree till it finds a definition. If it is never overridden will return the plain text error.
        """
        if self.parentHandler:
            return self.parentHandler.renderUnauthorized(request, exception)
        
        if request.method == "GET":
            return "Unauthorized Request: You are not authorized to view this information"
        else:
            return "Unauthorized Request: You are not authorized to edit this information"
