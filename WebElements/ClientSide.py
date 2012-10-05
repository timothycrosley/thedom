"""
    Convience python functions that return javascript code
"""

import json

def confirm(message, action):
    """
        Returns the javascript to present a confirm window to the user, before doing an action
    """
    return "if(window.confirm('%s')){%s}" % (message, action)

def callOpener(method):
    """
        Returns the javascript to run a command on a parent window
    """
    return """
            if(opener && !opener.closed)
            {
                try
                {
                    opener.%s;
                }
                catch(err)
                {
                }
            }
            """ % method

def updateParent():
    """
        Returns the javascript to call the updatedFromChild method on the parent window if present
    """
    return callOpener("updatedFromChild()")

def updateMultiple(controls):
    """
        Returns the javascript to update multiple page controls at once
    """
    if not controls:
        return ""

    if len(controls) == 1:
        return "ajaxUpdate('%s');" % controls[0]

    return "ajaxUpdate(%s);" % str(controls)

def focus(elementId, selectText=False):
    """
        Returns the javascript to focus on an input box based on id
    """
    if not selectText:
        return "WebElements.get('%s').focus();" % elementId
    return ("var inputElement = WebElements.get('%s');"
            "inputElement.focus();"
            "inputElement.select();") % elementId

def openPopup(url=None, width=700, height=700, normal=False, separateWindow=False, windowTitle="_blank"):
    """
        Returns the javascript to open a popup window
    """
    url = url and repr(url) or "this.href"
    return "Popup.open({url:%s, height:%d, width:%d, normal:%s, separateWindow:%s, name:'%s'});" % (url, int(height),
                                                                                         int(width),
                                                                                         normal and "true" or "false",
                                                                                  separateWindow and "true" or "false",
                                                                                  windowTitle)

def setValue(elementId, value):
    """
        Returns the javascript to set the value of an input element
    """
    return "WebElements.get('%s').value = %s;" % (elementId, repr(value))

def redirect(to):
    """
        Returns the javascript to change the location of the page
    """
    return "window.location = '%s';" % to

def showIfSelected(option, elementToShow):
    """
        Returns the javascript to only show the selected if it is selected
    """
    return """if (this.value == '%s'){
                        WebElements.show('%s');
                    }
                    else {
                        WebElements.hide('%s');
                    }
                """ % (option, elementToShow, elementToShow)

def showIfChecked(elementToShow):
    """
        Returns the javascript to only show an element if a certain checkbox is selected
    """
    return """if (this.checked){
                   WebElements.get('%s').disabled = '';
                }
                else {
                   WebElements.get('%s').disabled = 'true';
                }
            """ % (elementToShow, elementToShow)
