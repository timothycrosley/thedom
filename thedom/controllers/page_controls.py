'''
    PageControls.py

    Defines the most basic PageControls that can be subclassed to control sections of a page

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

import threading
import re
import copy

from . import HTTP
from .RequestHandler import RequestHandler
from thedom import UITemplate
from thedom.All import Factory
from thedom import Base
from thedom.Base import Node
from thedom.Layout import Center, Horizontal, Flow, Box
from thedom.Display import Image, Label, FormError
from thedom.Resources import ScriptContainer
from thedom.StringUtils import scriptURL
from thedom.Containers import PageControlPlacement
from thedom.Compile import CompiledTemplate
from thedom import ClientSide, UITemplate


class PageControl(RequestHandler, Node):
    """
        Defines the concept of a page control: The merger of a request handler and a Node
    """
    properties = Node.properties.copy()
    properties['autoLoad'] = {'action':'classAttribute', 'type':'bool'}
    tagName = "div"
    autoLoad = True
    autoReload = False
    silentReload = True
    elementFactory = Factory

    class ClientSide(Node.ClientSide):

        def get(self, silent=False, timeout=None, fresh=True, params=None, **kwargs):
            return ClientSide.call("DynamicForm.get", self, silent, params or scriptURL(kwargs), timeout, fresh)

        def getAll(self, controls, silent=False, timeout=None, fresh=True, params=None, **kwargs):
            return ClientSide.call("DynamicForm.get", controls, silent, params or scriptURL(kwargs), timeout, fresh)

        def postAll(self, controls, silent=False, timeout=None, fresh=False, params=None, **kwargs):
            return ClientSide.call("DynamicForm.post", controls, silent, params or scriptURL(kwargs), timeout,
                                   fresh)

        def post(self, silent=False, timeout=None, fresh=False, params=None, **kwargs):
            return ClientSide.call("DynamicForm.post", self, silent, params or scriptURL(kwargs), timeout, fresh)

        def putAll(self, controls, silent=False, timeout=None, fresh=False, params=None, **kwargs):
            return ClientSide.call("DynamicForm.put", controls, silent, params or scriptURL(kwargs), timeout, fresh)

        def put(self, silent=False, timeout=None, fresh=False, params=None, **kwargs):
            return ClientSide.call("DynamicForm.put", self, silent, params or scriptURL(kwargs), timeout, fresh)

        def delteAll(self, controls, silent=False, timeout=None, fresh=False, params=None, **kwargs):
            return ClientSide.call("DynamicForm.DELETE", controls, silent, params or scriptURL(kwargs), timeout, fresh)

        def delete(self, silent=False, timeout=None, fresh=False, params=None, **kwargs):
            return ClientSide.call("DynamicForm.DELETE", self, silent, params or scriptURL(kwargs), timeout, fresh)

        def move(self, to, makeTop=False):
            return ClientSide.move(self.id + ":Loading", to, makeTop)(Node.ClientSide.move(self, to, makeTop))

    class Loading(Center):
        """
            Defines how the element will look like while an AJAX call is being performed (unless silent loading is used)
            NOTE: you can override this whole class to modify the appearance - just replace with a different Node
        """
        def __init__(self, id, parent, **kwargs):
            Center.__init__(self, id, "", parent, **kwargs)
            self.addClass("WLoading")

            layout = self.addChildElement(Horizontal())
            layout.addClass("WContent")
            throbber = layout.addChildElement(Image(src="images/throbber.gif"))
            throbber.style['width'] = "34px"
            throbber.style['height'] = "32px"
            label = layout.addChildElement(Label())
            label.setText(self.parent.loadingText)

    class SpacedLoader(Box):
        width = 10
        height = 10

        def __init__(self, id, parent, **kwargs):
            Box.__init__(self, id, "", parent, **kwargs)
            box.style['width'] = "{0}px".format(self.width)
            box.style['height'] = "{0}px".format(self.height)

    def __init__(self, id=None, parent=None, parentHandler=None, initScripts=None, request=None, instanceOf=None,
                 **kwargs):
        if parentHandler:
            self.elementFactory = parentHandler.elementFactory

        RequestHandler.__init__(self, parentHandler=parentHandler, initScripts=initScripts, instanceOf=instanceOf)
        Node.__init__(self, id=id or self.accessor, name="", parent=None, **kwargs)
        self.setPrefix("")
        
        if id != self.accessor:
            self.attributes['handler'] = self.accessor

        self.request = request

        if instanceOf:
            self._loading = instanceOf._loading.replace(self.accessor, id)
            self.lock = None
            return

        self.lock = threading.Lock()
        self._loading = self.Loading(self.id + ":Loading", parent=self, hide=True).toHTML()
        controlScript = self.setScriptContainer(ScriptContainer()).content()
        if controlScript:
            self.initScripts.append(controlScript)

    def _registerAttribute(self, attributeName, attribute):
        """
            Compile templates on instantiation in addition to child controllers
        """
        if not RequestHandler._registerAttribute(self, attributeName, attribute):
            if isinstance(attribute, UITemplate.Template):
                setattr(self.__class__, attributeName, CompiledTemplate.create(attribute, self.elementFactory))
                return True

    def __call__(self, id, request, method="GET", autoLoad=None, autoReload=None, silentReload=None, **kwargs):
        """
            Call this to create a new instance of the page control - passing in a unique id
            and optionally a request or a dictionary of request fields
        """
        request = copy.copy(request)
        request.method = method
        if kwargs:
            request.fields = HTTP.FieldDict(request.fields.copy())
            request.fields.update(kwargs)

        id = self.accessor + str(id)
        request.fields['requestID'] = id
        instance = self.__class__(id=id, request=request, instanceOf=self)
        if autoLoad is not None:
            instance.autoLoad = autoLoad
        if autoReload is not None:
            instance.autoReload = autoReload
        if silentReload is not None:
            instance.silentReload = silentReload
        return instance

    def instanceID(self, salt="", element=""):
        """
            Returns what the instance ID would be for this controller or sub element given the provided salt value
        """
        return self.accessor + str(salt) + str(element)

    @property
    def loadingText(self):
        """
            Defines the default text to display while this controller is loading
        """
        return "Loading %s..." % (self.__class__.__name__, )

    def toHTML(self, formatted=False, *args, **kwargs):
        """
            Override toHTML to draw loading section in addition to controller placement
        """
        return "".join([self._loading, Node.toHTML(self, formatted, *args, **kwargs)])

    def buildElement(self, className, id=None, name=None, parent=None, scriptContainer=None, **kwargs):
        """
            Builds a Node using the factory attached to this controller
        """
        element = self.elementFactory.build(className, id, name, parent)
        if scriptContainer != None:
            element.setScriptContainer(scriptContainer)
        if kwargs:
            element.setProperties(kwargs)

        return element

    def buildTemplate(self, template):
        """
            Creates a Node from a template based on the pageControl's element factory
        """
        return template.build(self.elementFactory)

    def content(self, formatted=False, request=None, *args, **kwargs):
        """
            Overrides the Node content to include an initial response if autoLoad is set to true
        """
        request = request or HTTP.Request()
        if self.autoLoad == "AJAX":
            request.response.scripts.addScript("DynamicForm.get('%s');" % self.fullId())
        elif self.autoLoad == "silent":
            request.response.scripts.addScript("DynamicForm.get('%s', true);" % self.fullId())
        elif self.autoLoad is True:
            if not self._canView(request) or (request.method != "GET" and not self._canEdit(request)):
                request.response.status = HTTP.Response.Status.UNAUTHORIZED
                return self.renderUnauthorized(request)
            try:
                return self.rendered(request)
            except Exception as e:
                return self.renderInternalError(request, e)

        return ""

    def __str__(self):
        """
            Use the RequestHandler str implementation
        """
        return RequestHandler.__str__(self)
    
    def renderResponse(self, request, isCached=False):
        request = self.request or request
        
        requestID = request.fields.get('requestID')
        if requestID:
            if self.lock:
                self.lock.acquire()
            self.id = requestID

        ui = self.buildUI(request)
        self.initUI(ui, request)
        self._modifyUI(ui, request)
        if request.method != "GET":
            self.populateUI(ui, request)
        if self.autoReload:
            ui.clientSide(self.clientSide.get(silent=self.silentReload, timeout=self.autoReload))

        if request.method == "GET" and self.validGet(ui, request):
            self.processGet(ui, request)
        elif request.method == "POST" and self.validPost(ui, request):
            self.processPost(ui, request)
        elif request.method == "DELETE" and self.validDelete(ui, request):
            self.processDelete(ui, request)
        elif request.method == "PUT" and self.validPut(ui, request):
            self.processPut(ui, request)

        self.setUIData(ui, request)
        if not self.canEdit(request):
            ui.setEditable(False)
            
        if request.cacheKey:
            scriptContainer = ScriptContainer()
            oldScriptContainer = request.response.scripts
            request.response.scripts = scriptContainer
            ui.setScriptContainer(scriptContainer)
            to_return = ui.toHTML(request=request) + request.response.scripts.toHTML(request=request)
            request.cacheKey = False
            request.response.scripts = oldScriptContainer
        elif not request.response.scripts:
            scriptContainer = ScriptContainer()
            request.response.scripts = scriptContainer
            ui.setScriptContainer(scriptContainer)
            to_return = ui.toHTML(request=request) + scriptContainer.toHTML(request=request)
        else:
            ui.setScriptContainer(request.response.scripts)
            to_return = ui.toHTML(request=request)
            
        if requestID:
            self.id = self.accessor
            if self.lock:
                self.lock.release()
            
        return to_return

    def _modifyUI(self, ui, request):
        pass


class ElementControl(PageControl):
    """
        Defines a PageControl that is rendered using thedom
    """
    def buildUI(self, request):
        return Flow()

    def initUI(self, ui, request):
        """
            Adds all UI data that is needed independent of how the control processing goes
        """
        return

    def populateUI(self, ui, request):
        """
            Populates the UI with data from the request before processing begins, by default only done
            on none GET methods
        """
        ui.insertVariables(copy.deepcopy(request.fields))

    def setUIData(self, ui, request):
        """
            Sets the final UI data before rendering the UI and returning client-side
        """
        return

    def valid(self, ui, request):
        """
            The default validation method for all non get requests if validate(requestType) is not defined
        """
        if not request.method == "GET":
            return not ui.errors()
        else:
            return True

    def validPost(self, ui, request):
        """
            Returns true if the post data is valid
        """
        return self.valid(ui, request)

    def validGet(self, ui, request):
        """
            Returns true if the get data is valid - defaults to True should very rarely be overridden
        """
        return True

    def validDelete(self, ui, request):
        """
            Returns true if the delete data is valid
        """
        return self.valid(ui, request)

    def validPut(self, ui, request):
        """
            Returns true if the put data is valid
        """
        return self.valid(ui, request)

    def processPost(self, ui, request):
        """
            Override to define the processing specific to a post
        """
        pass

    def processGet(self, ui, request):
        """
            Override to define the processing specific to a get
        """
        pass

    def processDelete(self, ui, request):
        """
            Override to define the processing specific to a delete
        """
        pass

    def processPut(self, ui, request):
        """
            Override to define the processing specific to a put
        """
        pass


class TemplateControl(ElementControl):
    """
        Defines an ElementControl that is rendered from a WUI Template
        NOTE: When subclassing set the template attribute - aka template = UITemplate.fromFile("myFile.wui")
    """
    template = UITemplate.Template("empty")

    class TemplateLoader(Node):
        def __init__(self, id, parent, **kwargs):
            Node.__init__(self, id, "", parent, **kwargs)
            self += parent.template.build(parent.elementFactory)

    def __init__(self, id=None, parent=None, parentHandler=None, initScripts=None, **kwargs):
        ElementControl.__init__(self, id, parent, parentHandler, initScripts, **kwargs)
        self.autoRegister = []

    def _postConnections(self):
        """
            After all connections are made we automatically cache replacement actions where possible.
        """
        templateDefinition = self.template.build(self.elementFactory)
        for control in templateDefinition.allChildren():
            if isinstance(control, PageControl):
                self.registerControl(control.__class__)
            if isinstance(control, PageControlPlacement):
                self.autoRegister.append((control.id, self._findRelativeControl(control.control)))

    def _findRelativeControl(self, name):
        control = self
        if name.startswith(".."):
            control = control.parentHandler
            name = name[2:]
            while name.startswith("."):
                startFrom = control.parentHandler
                name = name[1:]

        for controlName in name.split("."):
            control = getattr(control, controlName)

        return control

    def buildUI(self, request):
        """
            Builds an instance of the defined template
        """
        return self.template.build(self.elementFactory)

    def _modifyUI(self, ui, request):
        """
            Automatically replaces any defined controls that exist on the template.
        """
        for controlAccessor, control in self.autoRegister:
            placement = getattr(ui, controlAccessor)
            if not placement or not placement.parent:
                continue

            placement.replaceWith(control)

