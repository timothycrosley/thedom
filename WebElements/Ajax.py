#!/usr/bin/python
"""
   Name:
       Ajax

   Description:
       Elements that ease the use of ajax
"""

import urllib

import Base
import Display
import Factory
import HiddenInputs
import Layout
from MethodUtils import CallBack
from Resources import ScriptContainer
from StringUtils import interpretAsString

Factory = Factory.Factory("AJAX")


class AJAXScriptContainer(ScriptContainer):
    """
        Defines a script container that will be executed via AJAX
    """
    tagName = "span"

    def __init__(self, id=None, name=None, parent=None, **kwargs):
        ScriptContainer.__init__(self, **kwargs)
        self.addClass("onLoadJavascript")
        self.hide()

    def content(self, formatted=False):
        """
            Overrides the base WebElement content method to replace non-safe characters
        """
        script = ScriptContainer.content(self, formatted=formatted)
        script = script.replace("&", "&amp;")
        script = script.replace("<", "&lt;")
        script = script.replace(">", "&gt;")
        return script

Factory.addProduct(AJAXScriptContainer)


class AjaxController(Layout.Box):
    """
        Abstract Page Controller Definition, separates a section of the page to update independent of the rest of the
        page using prototype.js AJAX convenience functions.
    """
    jsFunctions = ["ajaxUpdate", "ajaxDo", "ajaxParameters", "ajaxParametersMultiple",
                   "applyAjaxUpdate", "applyAjaxUpdateMultiple", "ajaxSubmit",
                   "_ajaxGet", "_ajaxGetMultiple", "abortAjaxUpdate", "_ajaxFields",
                   "_ajaxForms", "_ajaxSerialize"]

    autoload = True
    autoreload = False # set to a number of milliseconds if you want it to periodically reload
    callFunction = None # javascript function to call with JSON data
    hidden = False
    grabFields = []
    grabForms = []
    loadingText = "Loading..."

    class Loading(Layout.Box):
        """
            Defines what is shown in place of the controller while its content is loaded from the server
        """
        indicator = Display.Image(src='images/loop-grey.gif')

        def __init__(self, id, name=None, parent=None, loadingText=None, **kwargs):
            Layout.Box.__init__(self, id, name=None, parent=None, **kwargs)
            self.addChildElement(self.indicator, ensureUnique=False)
            self.label = self.addChildElement(Display.Label())
            self.label.setText(parent.loadingText)


    def __init__(self, id, name=None, parent=None, **kwargs):
        Layout.Box.__init__(self, id, name, parent, **kwargs)

        baseId = id
        self.index = 0

        self.id = id + "Controller"
        self.name = id + "Controller"

        if self.hidden:
            self.style['display'] = 'none'

        controller = HiddenInputs.HiddenValue(name="serverController")
        controller.setValue(baseId)
        self.addChildElement(controller)

        self.function = self.addChildElement(HiddenInputs.HiddenValue(name="callFunction"))

        content = Layout.Box(id)
        content.addClass(id)
        self.ajaxContent = self.addChildElement(content)
        self.ajaxContentText = self.ajaxContent.addChildElement(Base.TextNode())

        loading = self.Loading(id + ":Loading", parent=self)
        self.loadingBanner = self.addChildElement(loading)

        if self.autoload != "AJAX":
            loading.hide()

        self.defaultFields = loading.addChildElement(Layout.Box(id + ":Defaults"))
        self.defaultFields.hide()

        self.addJSFunctions(AjaxController)

        if self.autoload == "AJAX":
            self.addScript("ajaxUpdate('" + id + "');")
        if self.autoreload:
            self.addScript("setInterval('ajaxUpdate(\"" + id + "\", true)', " +
                           unicode(self.autoreload) + ");")

    @staticmethod
    def __urlStringFromDict__(parameterDict):
        params = []
        for key, value in parameterDict.iteritems():
            if type(value) in (list, set, tuple):
                for instance in value:
                    params.append("%s=%s" % (key, urllib.quote(interpretAsString(instance))))
            else:
                params.append("%s=%s" % (key, urllib.quote(interpretAsString(value))))

        return "&".join(params)

    def jsId(self, instanceId=None):
        """
            Returns the javascript that can be used to access this JSController, with instanceId representing
            it's instance on the page
        """
        return self.ajaxContent.fullId()

    @staticmethod
    def updateControls(controls, silent=True, parameters=None, timeout=0):
        """
            Returns the javascript to update a list of controls
        """
        if parameters == None:
            parameters = {}
        for index, control in enumerate(controls):
            if isinstance(control, Base.WebElement):
                controls[index] = control.jsId()
        return "ajaxUpdate(%s, %s, '%s', %d);" % (str(controls),
                                                interpretAsString(silent),
                                                AjaxController.__urlStringFromDict__(parameters), timeout)

    def update(self, silent=True, parameters=None, instanceId=None, timeout=0):
        """
            Returns the javascript that will update this control
        """
        if parameters == None:
            parameters = {}
        return "ajaxUpdate('%s', %s, '%s', %d);" % (self.jsId(instanceId),
                                                interpretAsString(silent),
                                                self.__urlStringFromDict__(parameters), timeout)

    def do(self, silent=True, parameters=None, instanceId=None):
        if parameters == None:
            parameters = {}
        return "ajaxDo('%s', %s, '%s');" % (self.jsId(instanceId),
                                            interpretAsString(silent),
                                            self.__urlStringFromDict__(parameters))

    def submit(self, silent=False, parameters=None, instanceId=None, timeout=0):
        """
            Returns the javascript that will submit this control
        """
        if parameters == None:
            parameters = {}
        return "ajaxSubmit('%s', %s, '%s', %d);" % (self.jsId(instanceId),
                                                interpretAsString(silent),
                                                self.__urlStringFromDict__(parameters), timeout)

    @staticmethod
    def _ajaxFields(view):
        return """
                var pageControl = WEAttribute(view + "Controller", "serverController");

                var fields = document.sharedFields;
                fields = fields.concat(document['sharedWith' + pageControl]);

                return fields;
                """

    @staticmethod
    def _ajaxForms(view):
        return """
                var pageControl = WEAttribute(view + "Controller", "serverController");

                var forms = Array();
                forms = forms.concat(document.sharedForms);
                forms = forms.concat(document["sharedFormsWith" + pageControl]);

                return forms;
               """

    @staticmethod
    def _ajaxSerialize(views, fields, forms, mode="update"):
        return """
                var parameters = Array();
                for(var currentField = 0; currentField < fields.length; currentField++){
                    field = WEGet(fields[currentField]);
                    if(field && field.name){
                        parameters.push(Form.Element.serialize(field));
                    }
                }
                for(var currentForm = 0; currentForm < forms.length; currentForm++){
                    var form = WEGet(forms[currentForm]);
                    if(form){
                        parameters = parameters.concat(Form.serialize(form).split("&"));
                    }
                }
                if(mode == "submit"){
                    parameters.push("processForm=true");
                }

                if(typeof(views) == typeof("")){
                    var controller = WEGet(views + "Controller");
                    var pageControl = WEAttribute(controller, "serverController");
                    parameters.push("pageControl=" + encodeURIComponent(pageControl));
                    parameters.push(Form.serialize(controller));
                }
                else if(typeof(views) == typeof([])){
                    for(currentView = 0; currentView < views.length; currentView++){
                        var view = views[currentView];
                        var controller = WEGet(view + "Controller");
                        var pageControl = WEAttribute(controller, "serverController");

                        parameters.push("pageControls=" + encodeURIComponent(pageControl));
                        parameters.push("pageControlView=" + encodeURIComponent(view));
                        parameters.push(encodeURIComponent(view) + "Form=" +
                                        WEReplaceAll(
                                            WEReplaceAll(Form.serialize(controller), "&", "[-AND-]"),
                                            "=", "[-EQUALS-]"));
                    }
                    parameters.push("pageControl=UpdateMultiple");
                }

                return parameters.join("&");
               """

    @staticmethod
    def ajaxParametersMultiple(views, mode="update"):
        return """
                var fields = Array();
                var forms = Array();
                for(currentView = 0; currentView < views.length; currentView++){
                    var view = views[currentView];
                    WECombine(fields, _ajaxFields(view));
                    WECombine(forms, _ajaxForms(view));
                }

                return _ajaxSerialize(views, fields, forms, mode);
               """

    @staticmethod
    def ajaxParameters(view, mode="update"):
        return "return _ajaxSerialize(view, _ajaxFields(view), _ajaxForms(view), mode);"

    @staticmethod
    def ajaxDo(view, silent=True, parameters=""):
        return """request = ajaxUpdate(view, silent, parameters);
                  if(typeof(view) == typeof("")){
                    setTimeout('abortAjaxUpdate("' + view + '");', 500);
                  }
                  else if(typeof(view) == typeof([])){
                    if(view.length == 1){
                        setTimeout('abortAjaxUpdate("' + view[0] + '");', 500);
                    }
                    else if(view.length > 1){
                        setTimeout('abortAjaxUpdate("' + view.join(",") + '");', 500);
                    }
                  }
               """

    @staticmethod
    def abortAjaxUpdate(view):
        return """if(loadingPageControls.hasOwnProperty(view) &&
                    loadingPageControls[view] != null){
                    if(loadingPageControls[view].abort)
                    {
                        loadingPageControls[view].abort();
                    }
                    clearTimeout(loadingPageControls[view]);
                  }"""

    @staticmethod
    def ajaxUpdate(view, silent=False, parameters="", timeout=0):
        return """if(typeof(view) == typeof("")){
                    if(timeout){
                        abortAjaxUpdate(view);
                        timeoutMethod = setTimeout("ajaxUpdate('" + view + "', " + silent + ", '" + parameters + "');", timeout);
                        timeoutMethod.abort = function abortTimeout(){};
                        loadingPageControls[view] = timeoutMethod
                    }
                    else{
                        return _ajaxGet(view, "update", silent, parameters);
                    }
                  }
                  else if(typeof(view) == typeof([])){
                    if(view.length == 1){
                        return ajaxUpdate(view[0], silent, parameters, timeout);
                    }
                    else if(view.length > 1){
                        if(timeout){
                            abortAjaxUpdate(view.join(','))
                            timeoutMethod = setTimeout("ajaxUpdate(['" + view.join("', '") + "'], " + silent + ", '" + parameters + "');", timeout);
                            timeoutMethod.abort = function abortTimeout(){};
                            loadingPageControls[view.join(',')] = timeoutMethod
                        }
                        else{
                            return _ajaxGetMultiple(view, "update", silent, parameters);
                        }
                    }
                  }"""

    @staticmethod
    def ajaxSubmit(view, silent=False, parameters="", timeout=0):
        return """if(typeof(view) == typeof("")){
                      if(timeout){
                        abortAjaxUpdate(view);
                        timeoutMethod = setTimeout("ajaxSubmit('" + view + "', " + silent + ", '" + parameters + "');", timeout);
                        timeoutMethod.abort = function abortTimeout(){};
                        loadingPageControls[view] = timeoutMethod
                      }
                      return _ajaxGet(view, "submit", silent, parameters);
                  }
                  else if(typeof(view) == typeof([])){
                    if(view.length == 1){
                        return _ajaxGet(view[0], "submit", silent, parameters);
                    }
                    else if(view.length > 1){
                        return _ajaxGetMultiple(view, "submit", silent, parameters);
                    }
                  }"""

    @staticmethod
    def _ajaxGetMultiple(views, mode, silent, parameters):
        return """
                servlet = WEGet('servletName').value;
                if(!silent){
                    for(currentView = 0; currentView < views.length; currentView++){
                        view = views[currentView];
                        WebElements.hide(view);
                        WebElements.show(view + ':Loading');
                    }
                }

                abortAjaxUpdate(views.join(','));

                var req = new Ajax.Updater('UpdateMultiple', servlet,
                                           {method:'post',
                                            parameters:ajaxParametersMultiple(views, mode) + "&" + parameters,
                                            key:views.join(','),
                                            onSuccess:function update(data)
                                            {
                                                applyAjaxUpdateMultiple(data, views, silent);
                                            }});

                loadingPageControls[views.join(',')] = req;
               """



    @staticmethod
    def applyAjaxUpdateMultiple(data, views, silent=False):
        return """
                applyAjaxUpdate(data, "UpdateMultiple", true);
                for(var currentView = 0; currentView < views.length; currentView++){
                    var view = views[currentView];
                    applyAjaxUpdate(data, view, silent);
                }
               """

    @staticmethod
    def _ajaxGet(view, mode, silent, parameters):
        return """
                servlet = WEGet('servletName').value;
                if(!silent){
                    WebElements.hide(view);
                    WebElements.show(view + ':Loading');
                }

                abortAjaxUpdate(view);

                var req = new Ajax.Updater(view, servlet,
                                        {method:"post",
                                            parameters:ajaxParameters(view, mode) + "&" + parameters,
                                            key:view,
                                            onSuccess:function update(data)
                                            {
                                                applyAjaxUpdate(data, view, silent);
                                            }});

                loadingPageControls[view] = req;
                return req;"""

    @staticmethod
    def applyAjaxUpdate(data, view, silent=False):
        return """
                if(!silent){
                    WebElements.show(view);
                }
                loadingPageControls[view] = null;
                WebElements.hide(view + ':Loading');
                var view = WEGet(view);
                childElements = WEChildElements(view);
                setTimeout("WEDoInPageJavascript('" + view.id + "');", 10);
                defaults = document.getElementById(view.id + ":Defaults");
                if(defaults){
                    WebElements.removeElement(defaults);
                }
                //alert(document.activeElement.tagName);
                if(document.activeElement && (document.activeElement.tagName.toLowerCase() == "input" ||
                                              document.activeElement.tagName.toLowerCase() == "textarea") &&
                   document.activeElement.type.toLowerCase() != "button" &&
                   document.activeElement.type.toLowerCase() != "submit")
                {
                    var lastSelectedId = document.activeElement.id;
                    if(lastSelectedId){
                        setTimeout("var element = WEGet('" + lastSelectedId + "'); element.focus();", 10);
                    }
                    if(document.activeElement.type == "text"){
                        var selectStart = document.activeElement.selectionStart;
                        var selectEnd = document.activeElement.selectionEnd;
                        if(selectStart != selectEnd){
                            setTimeout("WESelectText('" + lastSelectedId + "', " + selectStart + ", " + selectEnd + ");", 11);
                        }
                   }
                }

                var callFunction = WEAttribute(view.id + "Controller", "callFunction");
                if(callFunction){
                    setTimeout(callFunction + "(document.JSONDATA);document.JSONDATA = null;", 11);
                }
               """

    def insertVariables(self, fieldDict):
        """
            You can not insert variables into a page controller
        """
        pass

Factory.addProduct(AjaxController)
Loading = AjaxController.Loading


class ControlInstance(Base.WebElement):
    """
        Defines an instance of a control with the ability to pre-render it, and define its field dictionary
    """
    def __init__(self, control, initialContent=None, parent=None, defaultValues=None):
        Base.WebElement.__init__(self, parent=parent)

        self.control = control
        self.initialContent = initialContent
        self.defaultValues = defaultValues
        if self.initialContent:
            self.addChildElement(self.initialContent)

    def toHtml(self, formatted=False, *args, **kwargs):
        if self.initialContent:
            self.control.ajaxContent.addChildElement(self.initialContent).parent = self
        content = self.control.toHtml(formatted=formatted, *args, **kwargs)
        self.control.ajaxContent.reset()

        return content
