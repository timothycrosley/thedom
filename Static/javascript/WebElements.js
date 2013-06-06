/* WebElementUtils
 *
 * Contains general functions which ease the usage of multi-browser Javascript coding
 * Is a self contained namespaced library so it can interact well with other javascript libraries
 *
 */

//Provide a mapping of all commonly used keys under Keys.KEY_NAME
var Keys = Keys || {}
Keys.SPACE = 32;
Keys.ENTER = 13;
Keys.TAB = 9;
Keys.ESC = 27;
Keys.BACKSPACE = 8;
Keys.SHIFT = 16;
Keys.CONTROL = 17;
Keys.ALT = 18;
Keys.CAPSLOCK = 20;
Keys.NUMLOCK = 144;
Keys.LEFT = 37;
Keys.UP = 38;
Keys.RIGHT = 39;
Keys.DOWN = 40;
Keys.HOME = 36;
Keys.END = 35;
Keys.PAGE_UP = 33;
Keys.PAGE_DOWN = 34;
Keys.INSERT = 45;
Keys.DELETE = 46;
Keys.FUNCTIONS = [112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123];
Keys.NUMBERS = [48, 49, 50, 51, 52, 53, 54, 55, 56, 57];

var MessageTypes = MessageTypes || {}
MessageTypes.ERROR = "error";
MessageTypes.INFO = "info";
MessageTypes.WARNING = "warning";
MessageTypes.SUCCESS = "success";
MessageTypes.CLASSES = {"error":"WError", "info":"WInfo", "warning":"WWarning", "success":"WSuccess"};
MessageTypes.CLASS_LIST = ["WError", "WInfo", "WWarning", "WSuccess"];

//Provide basic platform information under Platform name-space
var Platform = Platform || {}
Platform.IS_IOS = /Apple.*Mobile/.test(navigator.userAgent)
Platform.IS_OPERA = Object.prototype.toString.call(window.opera) == '[object Opera]';
Platform.IS_IE = navigator.appVersion.match(/\bMSIE\b/) && !!window.attachEvent && !Platform.IS_OPERA;
Platform.IS_WEBKIT = navigator.userAgent.indexOf('AppleWebKit/') > -1
Platform.IS_GECKO = navigator.userAgent.indexOf('Gecko') > -1 && navigator.userAgent.indexOf('KHTML') === -1
Platform.HAS_PLACEHOLDERS = (!Platform.IS_IE || 'placeholder' in document.createElement('input'));

//Provides basic event handling
var Events = Events || {}

Events.addEvent = function(element, type, handler)
{
    var element = WebElements.get(element);

    if(typeof(type) == typeof([]))
    {
        return WebElements.forEach(type, function(eventType){Events.addEvent(element, eventType, handler);});
    }
    if(typeof(handler) == typeof([]))
    {
        return WebElements.forEach(handler, function(eventHandler){Events.addEvent(element, type, eventHandler);});
    }
    if (element.addEventListener)
    {
        element.addEventListener(type, handler, false);
    }
    else
    {
        if (!handler.$$guid)
        {
            handler.$$guid = Events.addEvent.guid++;
        }
        if (!element.events)
        {
            element.events = {};
        }

        var handlers = element.events[type];
        if (!handlers)
        {
            handlers = element.events[type] = {};
            if (element["on" + type])
            {
                handlers[0] = element["on" + type];
            }
        }
        handlers[handler.$$guid] = handler;
        element["on" + type] = Events.handleEvent;
    }
};
Events.addEvent.guid = 1;

Events.removeEvent = function(element, type, handler)
{
    var element = WebElements.get(element);

    if(typeof(type) == typeof([]))
    {
        return WebElements.forEach(type, function(eventType){Events.removeEvent(element, eventType, handler);});
    }
    if(typeof(handler) == typeof([]))
    {
        return WebElements.forEach(handler, function(eventHandler){Events.removeEvent(element, type, eventHandler);});
    }
    if (element.removeEventListener)
    {
        element.removeEventListener(type, handler, false);
    }
    else
    {
        if (element.events && element.events[type])
        {
            delete element.events[type][handler.$$guid];
        }
    }
};

Events.handleEvent = function(event)
{
    var returnValue = true;
    event = event || Events.fixEvent(((this.ownerDocument || this.document || this).parentWindow || window).event);
    var handlers = this.events[event.type];
    for (var i in handlers)
    {
        this.$$handleEvent = handlers[i];
        if (this.$$handleEvent(event) === false)
        {
            returnValue = false;
        }
    }
    return returnValue;
};

Events.fixEvent = function(event)
{
    event.preventDefault = Events.preventDefault;
    event.stopPropagation = Events.stopPropagation;
    return event;
};

Events.preventDefault = function()
{
    this.returnValue = false;
};

Events.stopPropagation = function()
{
    this.cancelBubble = true;
};

//Create main WebElement name space - pulling in Keys and Platform name space's
var WebElements = WebElements || {}
WebElements.Keys = Keys;
WebElements.Platform = Platform;
WebElements.Events = Events;

WebElements.Settings = {}
WebElements.Settings.throbberImage = 'images/throbber.gif';
WebElements.Settings.showImage = 'images/show.gif';
WebElements.Settings.hideImage = 'images/hide.gif';
WebElements.Settings.throbberHeight = 32;
WebElements.Settings.throbberWidth = 34;
WebElements.Settings.Serialize = ['input', 'textarea', 'select'];

WebElements.State = {}
WebElements.State.isPopupOpen = false;
WebElements.State.currentDropDown = null;
WebElements.State.currentButton = null;

//Returns the element given (if it is a page element) or the result of getElementId
WebElements.get = function (element)
{
    //If an actual element is given (or nothing is given) just return it
    if(!element || element.innerHTML != null || element == document || element == window)
    {
        return element;
    }

    //If a element id is given -- return the element associated with the id
    var idElement = document.getElementById(element);
    if(idElement != null && idElement.innerHTML != null)
    {
        return idElement;
    }

    //If a element name is given -- return the first element associated with the name
    var nameElement = document.getElementsByName(element);
    if(nameElement.length != 0 && nameElement[0].innerHTML != null)
    {
        return nameElement[0]
    }

    return null;
}

//Calls a callback method for each item in a list
WebElements.forEach = function(arrayOfItems, callBack)
{
    if(arrayOfItems.forEach)
    {
        return arrayOfItems.forEach(callBack);
    }

    for(var currentItem=0; currentItem < arrayOfItems.length; currentItem++)
    {
        callBack(arrayOfItems[currentItem]);
    }
    return true;
}

//Calls a callback for each item in a list and returns an array of the results
WebElements.map = function(arrayOfItems, callBack)
{
    if(arrayOfItems.map)
    {
        return arrayOfItems.map(callBack);
    }

    newArray = []
    for(var currentItem=0; currentItem < arrayOfItems.length; currentItem++)
    {
        newArray.push(callBack(arrayOfItems[currentItem]));
    }
    return newArray;
}

//Returns a list of nodes sorted by placement in the dom
WebElements.sortElements = function(elements)
{
    firstNode = elements[0];
    if(!firstNode)
    {
        return [];
    }
    if(firstNode.sourceIndex)
    {
        elements.sort(function(first, second){return first.sourceIndex - second.sourceIndex;});
    }
    else if(firstNode.compareDocumentPosition)
    {
        elements.sort(function(first, second){return 3 - (first.compareDocumentPosition(second) & 6)});
    }
    return elements;
}

//Returns a list of sorted and unique elements
WebElements.sortUnique = function(elements)
{
    var elements = WebElements.sortElements(elements);
    var lastAdded = null;
    return WebElements.getByCondition(function(element)
                                      {
                                        if(element !== lastAdded)
                                        {
                                            lastAdded = element;
                                            return true
                                        }
                                        return false;
                                      }, elements);
}

//An optimized way to getElements that match against a list of tagNames
WebElements.getElementsByTagNames = function(tagNames, parentElement, unsorted)
{
    var parentElement = WebElements.get(parentElement);
    var results = [];
    WebElements.forEach(tagNames, function(tagName){
        WebElements.forEach(parentElement.getElementsByTagName(tagName),
                            function(item){results.push(item);})});

    if(!unsorted)
    {
        return WebElements.sortElements(results)
    }

    return results;
}

//Returns elements that pass a conditional callback, optionally returning on the first match
WebElements.getByCondition = function(conditional, parentNode, stopOnFirstMatch)
{
    if(!stopOnFirstMatch){stopOnFirstMatch = false;}
    var elements_to_return = [];
    var elements = [];
    if(parentNode instanceof Array)
    {
        elements = parentNode;
    }
    else
    {
        parentNode = WebElements.get(parentNode);
        elements = parentNode.getElementsByTagName("*");
    }

    for(var currentElement=0; currentElement < elements.length; currentElement++)
    {
        element = elements[currentElement];
        if(conditional(element))
        {
            if(stopOnFirstMatch)
            {
                return element;
            }
            elements_to_return.push(element);
        }
    }

    return elements_to_return;
}

//Gets an element and returns its value
WebElements.getValue = function(element)
{
    var element = WebElements.get(element)
    return element && element.value || ""
}

//Hides Elements with a particular class name
WebElements.hideClass = function(className, parentNode)
{
    WebElements.forEach(WebElements.getElementByClassName(className, parentNode), WebElements.hide);
}

//Shows Elements with a particular class name
WebElements.showClass = function(className, parentNode)
{
    WebElements.forEach(WebElements.getElementByClassName(className, parentNode), WebElements.show);
}

//Creates a throbber on the fly, change WebElements.Settings.throbberImage to change image file
WebElements.buildThrobber = function()
{
    var throbber = document.createElement('img');
    throbber.src = WebElements.Settings.throbberImage;
    throbber.style.height = WebElements.Settings.throbberHeight + "px"
    throbber.style.width = WebElements.Settings.throbberWidth + "px"
    return throbber;
}

//Replaces an element with a throbberImage on the fly
WebElements.becomeThrobber = function(element)
{
    var element = WebElements.get(element);
    var throbber = WebElements.buildThrobber();
    var elementHeight = element.offsetHeight;
    var elementWidth = element.offsetWidth;

    throbber.style.padding = null;
    throbber.style.margin = null;
    throbber.style.backgroundColor = "white";
    throbber.style.border = "1px gray solid";


    throbber.className = element.className;
    throbber.style.height = elementHeight + "px";
    throbber.style.width = elementWidth + "px";

    var toReturn = WebElements.replace(element, throbber);

    if(elementHeight > WebElements.Settings.throbberHeight)
    {
        var half = String((elementHeight - WebElements.Settings.throbberHeight) / 2) + "px";
        throbber.style.paddingTop = half;
        throbber.style.paddingBottom = half;
    }

    if(elementWidth > WebElements.Settings.throbberWidth)
    {
        var half = String((elementWidth - WebElements.Settings.throbberWidth) / 2) + "px";
        throbber.style.paddingLeft = half;
        throbber.style.paddingRight = half;
    }

    return toReturn;
}

//Gets elements by there css class that are childern of a certain node - uses native implementation if present
WebElements.getElementsByClassName = function(className, parentNode, stopOnFirstMatch)
{
    parentNode = WebElements.get(parentNode);
    if(document.getElementsByClassName){
        var results = null;
        if(parentNode)
        {
            results = parentNode.getElementsByClassName(className);
        }
        else
        {
            results = document.getElementsByClassName(className);
        }
        if(stopOnFirstMatch)
        {
            return results[0];
        }
    }
    if(!parentNode)
    {
        parentNode = document.getElementsByTagName("body")[0];
    }

    var regexp = new RegExp('\\b' + className + '\\b');
    return WebElements.getByCondition(function(element){return regexp.test(element.className)},
                                      parentNode, stopOnFirstMatch);
}

//Gets the first element in parent node with a certain class name
WebElements.getElementByClassName = function(className, parentNode)
{
    return WebElements.getElementsByClassName(className, parentNode, true);
}

//Returns all children with a particular attribute value
WebElements.getChildrenByAttribute = function(parentNode, attributeName, attributeValue)
{
    return WebElements.getByCondition(function(element){return element[attributeName] === attributeValue;}, parentNode);
}

//Returns the first child with a particular attribute value
WebElements.getChildByAttribute = function(parentNode, attributeName, attributeValue)
{
    return WebElements.getByCondition(function(element){return element[attributeName] === attributeValue;}, parentNode,
                                      true);
}

//Returns children of an element by their name
WebElements.getChildrenByName = function(parentNode, name)
{
    return WebElements.getByCondition(function(element){return element.name == name}, parentNode);
}

//Returns a child of an element by its name
WebElements.getChildByName = function(parentNode, name)
{
    return WebElements.getByCondition(function(element){return element.name == name}, parentNode, true);
}

//populates a form using an id/name:value dictionary -- such as a request dictionary.
WebElements.populate = function(fieldDict)
{
    for(fieldId in fieldDict)
    {
        field = WebElements.get(fieldId);
        value = fieldDict[fieldId];
        if(field)
        {
            field.value = value;
        }
    }
}

//updates a countdown label slowly deincrementing till reaches 0 than calls action
WebElements.countDown = function(label, seconds, action)
{
    var label = WebElements.get(label);
    label.innerHTML = seconds;
    label.timeoutList = []

    for(var currentCount = 1; currentCount < seconds; currentCount++)
    {
        timeout = setTimeout('WebElements.get(\'' + label.id + '\').innerHTML = ' +
                  (seconds - currentCount) + ';', (currentCount * 1000));
        label.timeoutList.push(timeout);
    }

    timeout = setTimeout('WebElements.get(\'' + label.id + '\').innerHTML = 0;' +
                         action, seconds * 1000);
    label.timeoutList.push(timeout);
}

//updates a countdown label slowly deincrementing till reaches 0 than calls action
WebElements.abortCountDown = function(label)
{
    WebElements.forEach(WebElements.get(label).timeoutList, clearTimeout);
}

//Returns the number of pixels left of element
WebElements.pixelsToLeft = function(element)
{
    var aTag = WebElements.get(element);

    var pixelsToLeft = 0;
    do
    {
        pixelsToLeft += aTag.offsetLeft;
        aTag = aTag.offsetParent;
    } while(aTag && aTag.tagName!="BODY");

    var aTag = element.parentNode;
    do
    {
        if(aTag.scrollLeft)
        {
            pixelsToLeft -= aTag.scrollLeft;
        }
        aTag = aTag.parentNode;
    } while(aTag && aTag.tagName!="BODY");

    return pixelsToLeft;
}

//Returns the number of pixels above an element
WebElements.pixelsAbove = function(element)
{
    var aTag = WebElements.get(element);

    var pixelsAbove = 0;
    do
    {
        pixelsAbove += aTag.offsetTop;
        aTag = aTag.offsetParent;
    } while(aTag && aTag.tagName!="BODY");

    var aTag = element.parentNode;
    do
    {
        if(aTag.scrollTop)
        {
            pixelsAbove -= aTag.scrollTop;
        }
        aTag = aTag.parentNode;
    } while(aTag && aTag.tagName!="BODY");

    return pixelsAbove;
}

//Sets an element position to that of its parents + pixelsDown & pixelsToRight
WebElements.setAbsoluteRelativeToParent = function(element, pixelsDown, pixelsToRight, parentElement)
{
    var element = WebElements.get(element);
    if(!parentElement){parentElement = element.parentNode;}
    if(!pixelsDown){pixelsDown = 0;}
    if(!pixelsToRight){pixelsToRight = 0;}

    var parentElement = WebElements.get(parentElement);
    element.style.left = WebElements.pixelsToLeft(parentElement) + pixelsToRight;
    element.style.top = WebElements.pixelsAbove(parentElement) + pixelsDown;
}

//Sets an element position to that of its parents + pixelsDown & pixelsToRight
WebElements.displayDropDown = function(dropDown, parentElement)
{
    var dropDownElement = WebElements.get(dropDown);
    if(!parentElement){parentElement = dropDownElement.parentNode;}
    var parentElement = WebElements.get(parentElement);

    WebElements.setAbsoluteRelativeToParent(dropDownElement, parentElement.offsetHeight -1,
                                  0, parentElement);
    WebElements.show(dropDownElement);
}

//Toggles the displayed state of a drop down menu
WebElements.toggleDropDown = function(dropDown, parentElement)
{
    var dropDown = WebElements.get(dropDown);
    if(WebElements.shown(dropDown))
    {
        WebElements.hide(dropDown);
        return false;
    }
    WebElements.displayDropDown(dropDown, parentElement);
    return true;
}

WebElements.openAccordion = function(accordionName)
{
    WebElements.show(WebElements.getElementByClassName('AccordionContent', accordionName));
    WebElements.get(accordionName + 'Value').value = 'True';
    WebElements.get(accordionName + 'Image').src = 'images/hide.gif';
}

WebElements.fellowChild = function(element, parentClass, childClass)
{
    return WebElements.getElementByClassName(childClass, WebElements.parent(element, parentClass));
}

WebElements.fellowChildren = function(element, parentClass, childClass)
{
    return WebElements.getElementsByClassName(childClass, WebElements.parent(element, parentClass));
}

//Get first child element (exluding empty elements)
WebElements.firstChild = function(element)
{
    var element = WebElements.get(element);
    if(element.firstChild)
    {
        element = element.firstChild
        while ((!element || element.innerHTML == null) && element.nextSibling)
        {
            element = element.nextSibling;
        }
        return element;
    }
}

//Get last child element (exluding empty elements)
WebElements.lastChild = function(element)
{
    var element = WebElements.get(element);
    if(element.lastChild)
    {
        element = element.lastChild
    }
    while ((!element || element.innerHTML == null) && element.prevSibling)
    {
        element = element.prevSibling;
    }
    return element;
}


//Gets the next sibling (ignoring empty elements)
WebElements.next = function(element)
{
    var element = WebElements.get(element);
    var originalElement = element;
    if(element.nextSibling)
    {
        element = element.nextSibling;
    }
    while ((!element || element.innerHTML == null) && element.nextSibling)
    {
        element = element.nextSibling;
    }
    return element;
}

//Gets the previous sibling (ignoring empty elements)
WebElements.prev = function(element)
{
    var element = WebElements.get(element);
    if(element.previousSibling)
    {
        element = element.previousSibling;
    }
    while ((!element || element.innerHTML == null) && element.previousSibling)
    {
        element = element.previousSibling;
    }
    return element;
}

//increments the value of a hiddenField
WebElements.increment = function(element, max)
{
    var element = WebElements.get(element);
    var number = (parseInt(element.value) || 0) + 1;
    if(max != undefined && number > max){
        number = max;
    }
    element.value = number;
    element.onchange && element.onchange();
}

//deincrements the value of a hiddenField
WebElements.deincrement = function(element, min)
{
    var element = WebElements.get(element);
    var number = (parseInt(element.value) || 0) - 1;
    if(min != undefined && number < min){
        number = min;
    }
    element.value = number;
    element.onchange && element.onchange();
}

//Sets the prefix for the container and all childElements
WebElements.setPrefix = function(container, prefix)
{
    var container = WebElements.get(container);
    container.id = prefix + container.id;
    container.name = prefix + container.name;

    WebElements.forEach(WebElements.childElements(container), function(child){
            child.id = prefix + child.id;
            child.name = prefix + child.name;});
}

//Gets a parent element based on its class name or alternatively giving up when it hits a particular class
WebElements.parent = function(element, className, giveUpAtClass)
{
    var element = WebElements.get(element);
    var regexp = new RegExp('\\b' + className + '\\b');
    var regexpCancel = false;
    if(giveUpAtClass)
    {
        regexpCancel = new RegExp('\\b' + giveUpAtClass + '\\b');
    }

    if(element.parentNode)
    {
        element = element.parentNode;
    }
    while ((!element || element.innerHTML == null || !regexp.test(element.className))
           && element.parentNode)
    {
        element = element.parentNode;
        if(regexpCancel && regexpCancel.test(element.className)){
            return false;
        }
    }
    return element;
}


//Removes all children
WebElements.clearChildren = function(element, replacement)
{
    var element = WebElements.get(element)
    WebElements.forEach(WebElements.childElements(element), function(element){WebElements.remove(element)});
    if(replacement)
    {
        element.appendChild(replacement)
    }
}

//Allows you to get a list of all non empty childElements
WebElements.childElements = function(parentElement)
{
    return WebElements.getByCondition(function(element){return element && element.innerHTML}, parentElement)
}

//Allows you to get an element in the same location on the tree based on a classname
WebElements.peer = function(element, className)
{
    return WebElements.getElementByClassName(className, WebElements.get(element).parentNode);
}

//Allows you to get elements in the same location on the tree based on a classname
WebElements.peers = function(element, className)
{
    return WebElements.getElementsByClassName(className, WebElements.get(element).parentNode);
}


//Forces this to be the only peer with class
WebElements.stealClassFromPeer = function(element, className)
{
    WebElements.forEach(WebElements.peers(element, className),
                                         function(element){WebElements.removeClass(element, className)});
    WebElements.addClass(element, className);
}

//Forces this to be the only peer with class
WebElements.stealClassFromFellowChild = function(element, parentClassName, className)
{
    WebElements.forEach(WebElements.fellowChildren(element, parentClassName, className),
                        function(element){WebElements.removeClass(element, className);});
    WebElements.addClass(element, className);
}

//Removes the class from all elements in the specified container and sets it on itself
WebElements.stealClassFromContainer = function(element, container, className)
{
    WebElements.forEach(WebElements.getElementsByClassName(className, container),
                        function(element){WebElements.removeClass(element, className)});
    WebElements.addClass(element, className);
}

//hides an element by setting its display property to none
WebElements.hide = function(element)
{
    var element = WebElements.get(element);
    if(element != null)
    {
        element.style.display = "none";
        return true;
    }
    return false;
}

//shows an element by setting its display property to block
WebElements.show = function(element)
{
    var element = WebElements.get(element);
    if(element != null)
    {
       element.style.display = "";
        return true;
    }
    return false;
}

//shows the element if it is hidden - hides it if it is visable
WebElements.toggleVisibility = function(element)
{
    var element = WebElements.get(element);
    WebElements.shown(element) && WebElements.hide(element) || WebElements.show(element);
}

//return if the element is visable or not
WebElements.shown = function(element)
{
    element = WebElements.get(element);
    if(!element || element.style.display == "none")
    {
        return false;
    }
    return true;
}

//replaces 'element' with 'newElement' (element must contain a parent element)
WebElements.replace = function(element, newElement)
{
   var element = WebElements.get(element);
   var elementParent = element.parentNode;
   if(!elementParent)
   {
       return false;
   }
   elementParent.replaceChild(WebElements.get(newElement), element);
   return true;
}

//removes 'element' from the page (element must contain a parent element)
WebElements.remove = function(element)
{
    var element = WebElements.get(element);
    var elementParent = element.parentNode;
    if(!elementParent)
    {
        return false;
    }

    elementParent.removeChild(element);
    return true;
}

//clears the innerHTML of an element
WebElements.clear = function(element)
{
    WebElements.get(element).innerHTML = "";
}

//adds an option to a selectbox with a specified name and value
WebElements.addOption = function(selectElement, optionName, optionValue)
{
    if(!optionValue){optionValue = optionName}

    var newOption = document.createElement('option');
    newOption.innerHTML = optionName;
    newOption.value = optionValue;
    WebElements.get(selectElement).appendChild(newOption);
}

//adds a list of options option to a selectbox with a specified name/value
WebElements.addOptions = function(selectElement, options)
{
    var selectElement = WebElements.get(selectElement);
    WebElements.forEach(options, function(option){WebElements.addOption(selectElement, option);})
}

//adds html to element
WebElements.addHtml = function(element, html)
{
    var newDiv = document.createElement('div');
    newDiv.innerHTML = html;
    WebElements.get(element).appendChild(newDiv);
    return newDiv
}

//moves an element to a new location
WebElements.move = function(element, to, makeTop)
{
    var sendTo = WebElements.get(to);
    if(makeTop)
    {
        var firstChild = WebElements.firstChild(sendTo);
        if(firstChild)
        {
            return sendTo.insertBefore(WebElements.get(element), firstChild);
        }
    }
    return sendTo.appendChild(WebElements.get(element));
}

//makes a copy of an element into 'to' and returns the copy optionally incrementing its ID
WebElements.copy = function(element, to, incrementId)
{
    if(incrementId == null){incrementId = false;}

    var elementCopy = WebElements.get(element).cloneNode(true);
    var toReplace = elementCopy.id
    if(toReplace && incrementId)
    {
        for(currentChar = toReplace.length - 1; currentChar >= 0; currentChar--)
        {
            var character = toReplace[currentChar];
            if(isNaN(character))
            {
                break;
            }
        }
        var splitAt = currentChar + 1
        var increment = (toReplace.substring(splitAt, toReplace.length) * 1) + 1
        var replacement = toReplace.substring(0, splitAt) + increment
        elementCopy.id = replacement

        var html = elementCopy.innerHTML

    }
    WebElements.get(to).appendChild(elementCopy);

    if(incrementId)
    {
        elementCopy.innerHTML = WebElements.replaceAll(html, toReplace, replacement);
    }

    return elementCopy
}

//returns true if text WEContains subtext false if not
WebElements.contains = function(text, subtext, caseSensitive)
{
    if(!caseSensitive)
    {
        var text = text.toLowerCase();
        var subtext = subtext.toLowerCase();
    }

    return text.indexOf(subtext) != -1 && true || false
}

//returns true if any words within text start with subtext
WebElements.startsWith = function(text, subtext, caseSensitive)
{
    if(!caseSensitive)
    {
        var text = text.toLowerCase();
        var subtext = subtext.toLowerCase();
    }

    var text = WebElements.replaceAll(text, ">", " ");
    text = WebElements.replaceAll(text, "<", " ");
    text = WebElements.replaceAll(text, ",", " ");
    text = WebElements.replaceAll(text, "|", " ");
    text = text.split(" ")

    for(currentWord = 0; currentWord < text.length; currentWord++)
    {
        var word = text[currentWord]
        if(word.indexOf(subtext) == 0)
        {
            return true;
        }
    }

    return false;
}

//Adds a prefix to all child elements
WebElements.addPrefix = function(container, prefix)
{
    if(!caseSensitive)
    {
        var text = text.toLowerCase();
        var subtext = subtext.toLowerCase();
    }

    if(text.indexOf(subtext) == -1)
    {
        return false;
    }
    return true;
}

//sorts a list alphabetically by innerHTML
WebElements.sortSelect = function(selectElement, sortByValue)
{
    if(!sortByValue){sortByValue = false;}

    var selectElement = WebElements.get(selectElement);
    var selectOptions = selectElement.options;
    var sorted = new Array();
    var selectElementSorted = new Array();

    for(currentOption in selectedOptions)
    {
        var option = selectOptions[currentOption];
        if(sortByValue)
        {
            sorted[currentOption] = [option.value, option.innerHTML, option.id, option.disabled];
        }
        else
        {
            sorted[currentOption] = [option.innerHTML, option.value, option.id, option.disabled];
        }
    }

    sorted.sort();
    for(currentOption in sorted)
    {
        if(sortByValue)
        {
            selectElement.options[currentOption].value=sorted[currentOption][0];
            selectElement.options[currentOption].innerHTML=sorted[currentOption][1];
        }
        else
        {
            selectElement.options[currentOption].innerHTML=sorted[currentOption][0];
            selectElement.options[currentOption].value=sorted[currentOption][1];
        }
        selectElement.options[currentOption].id = sorted[currentOption][2];
        selectElement.options[currentOption].disabled = sorted[currentOption][3];
    }
}

//returns a list without duplicate elements
WebElements.removeDuplicates = function(inArray)
{
    var result = {};

    for(var i = 0; i < inArray.length; i++)
    {
      result[inArray[i]] = true;
    }

    var outArray = new Array();
    for(var dictKey in result)
    {
        outArray.push(dictKey)
    }

    return outArray;
}

//returns the selected options within a select box
WebElements.selectedOptions = function(selectBox)
{
    return WebElements.getByCondition(function(option){return option.selected}, WebElements.get(selectBox).options);
}

//Selects all element of a select box
WebElements.selectAllOptions = function(selectBox)
{
    WebElements.forEach(WebElements.get(selectBox).options, function(option){option.selected = true;});
}

//sets the options available for selection within a select box
WebElements.setOptions = function(selectBox, options)
{
    selectBox = WebElements.get(selectBox);
    WebElements.forEach(selectBox.options, WebElements.remove);
    WebElements.clear(selectBox);
    WebElements.addOptions(selectBox, options);
}

//returns the selected checkboxes withing a container
WebElements.selectedCheckboxes = function(container)
{
    return WebElements.getByCondition(function(element){return element.checked}, container);
}

WebElements.selectAllCheckboxes = function(container, check)
{
    WebElements.forEach(WebElements.getChildrenByAttribute(container, 'type', 'checkbox'),
                        function(child){child.checked = check;});
}

//returns all nested values within a contianer
WebElements.getValues = function(container, checkSelected, tagName)
{
    if(checkSelected == null){var checkSelected = false;}
    if(!tagName) {tagName = "option";}

    var container = WebElements.get(container);
    var optionElements = container.getElementsByTagName(tagName);

    var values = Array();
    for(currentOption = 0; currentOption < optionElements.length; currentOption++)
    {
        option = optionElements[currentOption];
        if (!checkSelected || option.selected || option.checked)
        {
            values.push(option.value)
        }
    }
    return values
}

//Get a child element of element based on value
WebElements.getElementByValue = function(element, value)
{
    return WebElements.getChildByAttribute(element, 'value', value);
}

//Get a child element of element based on value
WebElements.getElementByInnerHTML = function(element, html)
{
    return WebElements.getChildByAttribute(element, 'innerHTML', html);
}

//returns the first selected option within a select box
WebElements.selectedOption = function(selectBox)
{
    return WebElements.getByCondition(function(element){return element.selected;}, WebElements.get(selectBox).options,
                                      true);
}

//selects an element based on its value
WebElements.selectOption = function(selectBox, option)
{
    WebElements.selectedOption(selectBox).selected = false;
    WebElements.getElementByValue(selectBox, option).selected = true;
}

//replaces all instances of a string with another string
WebElements.replaceAll = function(string, toReplace, replacement)
{
    return string.split(toReplace).join(replacement);
}

//returns all css classes attached to an element as a list
WebElements.classes = function(element)
{
    var element = WebElements.get(element);
    if(!element)
    {
        return [];
    }
    var classes = element.className;
    return classes.split(" ");
}

//returns true if element contains class
WebElements.hasClass = function(element, className)
{
    var element = WebElements.get(element)
    var regexp = new RegExp('\\b' + className + '\\b');
    if(regexp.test(element.className))
    {
        return true;
    }
    return false;
}

//sets an elements classes based on the passed in list
WebElements.setClasses = function(element, classList)
{
    var element = WebElements.get(element);
    element.className = classList.join(" ");
}

//removes a css class
WebElements.removeClass = function(element, classToRemove)
{
    WebElements.setClasses(element, WebElements.removeFromArray(WebElements.classes(element), classToRemove));
}

//adds a css class
WebElements.addClass = function(element, classToAdd)
{
    var element = WebElements.get(element);
    var styleClasses = WebElements.classes(element);

    for(currentClass = 0; currentClass < styleClasses.length; currentClass++)
    {
        var styleClass = styleClasses[currentClass];
        if(styleClass == classToAdd)
        {
            return;
        }
    }

    element.className += " " + classToAdd;
}

//Removes all instances of an element from an array
WebElements.removeFromArray = function(arrayOfItems, toRemove)
{
    return WebElements.getByCondition(function(item){return item != toRemove}, arrayOfItems);
}

//lets you choose one class out of a list of class choices
WebElements.chooseClass = function(element, classes, choice)
{
    var element = WebElements.get(element);
    var styleClasses = WebElements.classes(element);
    for(currentClass = 0; currentClass < classes.length; currentClass++){
        styleClasses = WebElements.removeFromArray(styleClasses, classes[currentClass]);
    }
    styleClasses.push(choice);
    WebElements.setClasses(element, styleClasses);
}

// Forces the browser to redraw the element
WebElements.redraw = function(element)
{
    var parentElement = WebElements.get(element).parentNode;
    var html = parentElement.innerHTML;

    parentElement.innerHTML = "";
    parentElement.innerHTML = html;
}

//Strip spaces before and after string
WebElements.strip = function(string)
{
    return string.replace(/^\s+|\s+$/g,"");
}

WebElements.stripLeadingZeros = function(someStr)
{
   var someStr2 = String(someStr);
   if(someStr2 == '0')
       return someStr2;
   return someStr2.replace(/^[0]+/, '');
}

//Easy way to see if a value is contained in a list
WebElements.inList = function(list, value)
{
    for(var current = 0; current < list.length; current++)
    {
        if(list[current] == value)
        {
            return true;
        }
    }
    return false;
}

//Appens to a list only if the value is not already contained in the list
WebElements.appendOnce = function(list, listItem)
{
    if(!WebElements.inList(list, listItem))
    {
        list.push(listItem)
    }
}

//Combines two lists into one ignoring duplicate values
WebElements.combine = function(list, list2)
{
    for(var currentListItem = 0; currentListItem < list2.length; currentListItem++)
    {
        listItem = list2[currentListItem];
        WebElements.appendOnce(list, listItem);
    }
}

//suppress a single elements attribute (usually an event)
WebElements.suppress = function(element, attribute)
{
    var element = WebElements.get(element);

    element['suppressed_' + attribute] = element[attribute];
    element[attribute] = null;
}

//unsuppress a single elements attribute
WebElements.unsuppress = function(element, attribute)
{
    var element = WebElements.get(element);

    element[attribute] = element['suppressed_' + attribute];
    element['suppressed_' + attribute] = element[attribute];
}

WebElements.toggleMenu = function(button)
{
    var menu = WebElements.peer(button, 'WMenu');
    if(WebElements.State.currentDropDown != menu){
        WebElements.hide(WebElements.State.currentDropDown);
    }
    WebElements.State.currentDropDown = menu;
    WebElements.toggle(WebElements.State.currentDropDown);
}

WebElements.closeMenu = function()
{
    WebElements.hide(WebElements.State.currentDropDown);
    if(WebElements.State.currentButton){
        WebElements.removeClass(WebElements.State.currentButton, 'WSelected');
    }
}

WebElements.selectText = function(element, start, end)
{
    var element = WebElements.get(element);
    if(element.setSelectionRange){
        element.setSelectionRange(parseInt(start), parseInt(end));
    }
    else if (element.createTextRange){
        var range = element.createTextRange();
        range.collapse(true);
        range.moveStart('character', parseInt(start));
        range.moveEnd('character', parseInt(end - start));
        range.select();
    }
}

WebElements.openPopup = function(popupName, popupURL, width, height, normal, options)
{
    var popupName = WebElements.replaceAll(popupName, ' ', '');

    params = ["focus=true,scrollbars=yes,resizable=yes"]
    if(height)
    {
        params.push("height=" + height);
    }
    if(width)
    {
        params.push("width=" + width);
    }
    if(normal)
    {
        params.push("menubar=yes,status=yes,toolbar=yes,location=yes");
    }

    var newWindow = window.open(popupURL, popupName, params.join(","));

    if(window.focus)
    {
        newWindow.focus()
    }
    return false;
}

WebElements.scrolledToBottom = function(scroller)
{
    var scroller = WebElements.get(scroller);
    var oldScrollTop = scroller.scrollTop;
    scroller.scrollTop += 10;
    if (scroller.scrollTop != oldScrollTop)
    {
        scroller.scrollTop = oldScrollTop;
        return false
    }
    else
    {
        return true
    }
}

// Toggle between Adding or Removing a class from an element.
WebElements.toggleClass = function(element, className)
{
	if(WebElements.hasClass(element, className))
	{
		WebElements.removeClass(element, className);
	}
	else
	{
		WebElements.addClass(element, className);
	}
}

// Toggle between selecting/unselecting a row on a table.
WebElements.toggleTableRowSelect = function(input)
{
	var row = input
	for (var levels = 3; levels > 0; levels -= 1)
	{
		row = row.parentElement
		if (row.parentElement.tagName == "TR")
		{
			WebElements.toggleClass(row.parentElement, 'selected');
			levels = 0;
		}
	}
}

WebElements.getNotificationPermission = function()
{

    if (window.webkitNotifications)
    {
        if (window.webkitNotifications.checkPermission() != 0)
        {
            window.webkitNotifications.requestPermission();
        }
    }
}

WebElements.showNotification = function(title, content, icon)
{
    if(!icon){icon = "images/info.png";}

    if (window.webkitNotifications)
    {
        if (window.webkitNotifications.checkPermission() == 0)
        {
            var notification = window.webkitNotifications.createNotification(icon, title, content);
            notification.show();
            return notification;
        }
    }
}

// Make two checkboxes act like radio button. element is "this" and pair is the other checkbox
WebElements.checkboxActsLikeRadioButton = function(element, pair)
{
    var element = WebElements.get(element);
    var pair = WebElements.get(pair);
    if(!element.checked)
    {
        return;
    }
    pair.checked = false;
}

// Accepts an event performing no operation on it and stopping any further operations from taking place
WebElements.stopOperation = function(evt)
{
  evt.stopPropagation();
  evt.preventDefault();
}

WebElements.onPagerChange = function(pager, callBack)
{
    var pager = WebElements.get(pager);
    if(!pager)
    {
        return;
    }
    var indexElement = WebElements.get(pager.id + "Index")
    WebElements.forEach(WebElements.getElementsByTagNames(['a', 'input'], pager),
                        function(element){
                            WebElements.Events.addEvent(element, 'click', function(){
                                indexValue = '0';
                                if(element.getAttribute('index'))
                                {
                                    indexValue = element.getAttribute('index');
                                }
                                indexElement.value = indexValue;
                                WebElements.becomeThrobber(element);
                                callBack(WebElements.serializeAll(pager));
                            })});
}

WebElements.clickDropDown = function(menu, openOnly, button, parentElement)
{
    WebElements.State.isPopupOpen = true;
    if(WebElements.State.currentDropDown && WebElements.State.currentDropDown != menu)
    {
        WebElements.hide(WebElements.State.currentDropDown);
        WebElements.removeClass(WebElements.State.currentButton, 'WSelected');
    }
    WebElements.State.currentDropDown = menu;
    WebElements.State.currentButton = button;
    if(!openOnly || !WebElements.shown(WebElements.State.currentDropDown)){
        if(WebElements.toggleDropDown(WebElements.State.currentDropDown, parentElement)){
            WebElements.addClass(button, 'WSelected');
        }
        else{
            WebElements.removeClass(button, 'WSelected');
       }
   }
}

WebElements.addPlaceholders = function(element)
{
    if(Platform.HAS_PLACEHOLDERS)
    {
        return;
    }

    var element = WebElements.get(element);
    WebElements.forEach(element.getElementsByTagName('input'), function(input)
    {
        if(input.getAttribute('placeholder'))
        {
            input.style.cssText = "color:#939393;font-style:italic;"
            input.value = input.getAttribute("placeholder");
            input.onclick = function()
            {
                if(this.value == this.getAttribute("placeholder"))
                {
                    this.value = '';
                    this.style.cssText = "color:#000;font-style:normal;"
                }
            }
            input.onblur = function()
            {
                if(this.value == '')
                {
                    this.value = this.getAttribute("placeholder");
                    this.style.cssText = "color:#939393;font-style:italic;"
                }
            }
        }
    });
}


//attach on click event to body to close any open pop up menus when a random click is placed
WebElements.Events.addEvent(window, 'load', function()
{
    document.body.onclick = function closeOpenMenu()
    {
        if(WebElements.State.isPopupOpen)
        {
            WebElements.State.isPopupOpen = false;
        }
        else
        {
            WebElements.closeMenu();
            WebElements.State.isPopupOpen = false;
        }
    }
    WebElements.addPlaceholders(document);
});

WebElements.serialize = function(field)
{
    var element = WebElements.get(field);
    var tagName = element.tagName.toLowerCase();
    var key = encodeURIComponent(element.name);
    if(!key)
    {
        return '';
    }
    if(tagName == "input" || tagName == "textarea")
    {
        if(tagName == "input")
        {
            var type = element.type.toLowerCase();
            if(((type == "checkbox" || type == "radio") && !element.checked) || type == "button")
            {
                return '';
            }
        }
        return key + '=' + encodeURIComponent(element.value);
    }
    if(tagName == "select")
    {
        var value = [];
        WebElements.forEach(element.options, function(option){
                        if(option.selected){value.push(key + "=" + encodeURIComponent(option.value))}});
        return value.join("&");
    }
}

WebElements.serializeElements = function(elements)
{
    var params = []
    WebElements.forEach(elements,
                        function(item){result = WebElements.serialize(WebElements.get(item));
                                       if(result){params.push(result);}});
    return params.join("&");
}

WebElements.serializeAll = function(container)
{
    if(!container){container = document}

    var container = WebElements.get(container);
    return WebElements.serializeElements(WebElements.getElementsByTagNames(WebElements.Settings.Serialize, container));
}

//Presents a confirm window to the user, before doing an action
WebElements.confirm = function(message, action)
{
    if(window.confirm(message))
    {
        action();
    }
}

//Evaluates a method on the popup's opener
WebElements.callOpener = function(method)
{
    if(opener && !opener.closed)
    {
        try
        {
            eval("opener." + method + ";");
        }
        catch(err)
        {
        }
    }
}


//Tells the popup's opener that it has updated
WebElements.updateParent = function()
{
    return WebElements.callOpener("updatedFromChild()");
}

//Sets the focus to a specif element - optionally selecting text
WebElements.focus = function(element, selectText)
{
    var element = WebElements.get(element);
    element.focus();
    if(selectText)
    {
        element.select();
    }
}

//Sets the value of an element
WebElements.setValue = function(element, value)
{
    var element = WebElements.get(element).value = value;
}

//Shows the defined element only if the value matches
WebElements.showIfValue = function(element, value, elementToShow)
{
    var element = WebElements.get(element);
    if(element.value == value)
    {
        WebElements.show(elementToShow);
    }
    else
    {
        WebElements.hide(elementToShow);
    }
}

//Shows the defined element only if the checkbox is checked
WebElements.showIfChecked = function(checkbox, value, elementToShow)
{
    var checkbox = WebElements.get(checkbox);
    if(checkbox.checked)
    {
        WebElements.show(elementToShow);
    }
    else
    {
        WebElements.hide(elementToShow);
    }
}

//Expands a template written in the form of a python template
WebElements.expandTemplate = function(template, valueDictionary)
{
    var result = template;
    for(key in valueDictionary)
    {
        result = WebElements.replaceAll(template, "$" + key, valueDictionary[key]);
    }

    return result
}

{

    /*!
    * Pikaday
    *
    * Copyright © 2013 David Bushell | BSD & MIT license | https://github.com/dbushell/Pikaday
    */

    (function (root, define, factory)
    {
        'use strict';

        if (typeof define === 'function' && define.amd) {
            // AMD. Register as an anonymous module.
            define(function (req)
            {
                // Load moment.js as an optional dependency
                var id = 'moment';
                var moment = req.defined && req.defined(id) ? req(id) : undefined;
                return factory(moment || root.moment);
            });
        } else {
            // Browser global
            root.Pikaday = factory(root.moment);
        }
    }(window, window.define, function (moment)
    {
        'use strict';

        /**
        * feature detection and helper functions
        */
        var hasMoment = typeof moment === 'function',

        hasEventListeners = !!window.addEventListener,

        document = window.document,

        sto = window.setTimeout,

        addEvent = function(el, e, callback, capture)
        {
            if (hasEventListeners) {
                el.addEventListener(e, callback, !!capture);
            } else {
                el.attachEvent('on' + e, callback);
            }
        },

        removeEvent = function(el, e, callback, capture)
        {
            if (hasEventListeners) {
                el.removeEventListener(e, callback, !!capture);
            } else {
                el.detachEvent('on' + e, callback);
            }
        },

        fireEvent = function(el, eventName, data)
        {
            var ev;

            if (document.createEvent) {
                ev = document.createEvent('HTMLEvents');
                ev.initEvent(eventName, true, false);
                ev = extend(ev, data);
                el.dispatchEvent(ev);
            } else if (document.createEventObject) {
                ev = document.createEventObject();
                ev = extend(ev, data);
                el.fireEvent('on' + eventName, ev);
            }
        },

        trim = function(str)
        {
            return str.trim ? str.trim() : str.replace(/^\s+|\s+$/g,'');
        },

        hasClass = function(el, cn)
        {
            return (' ' + el.className + ' ').indexOf(' ' + cn + ' ') !== -1;
        },

        addClass = function(el, cn)
        {
            if (!hasClass(el, cn)) {
                el.className = (el.className === '') ? cn : el.className + ' ' + cn;
            }
        },

        removeClass = function(el, cn)
        {
            el.className = trim((' ' + el.className + ' ').replace(' ' + cn + ' ', ' '));
        },

        isArray = function(obj)
        {
            return (/Array/).test(Object.prototype.toString.call(obj));
        },

        isDate = function(obj)
        {
            return (/Date/).test(Object.prototype.toString.call(obj)) && !isNaN(obj.getTime());
        },

        isLeapYear = function(year)
        {
            // solution by Matti Virkkunen: http://stackoverflow.com/a/4881951
            return year % 4 === 0 && year % 100 !== 0 || year % 400 === 0;
        },

        getDaysInMonth = function(year, month)
        {
            return [31, isLeapYear(year) ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month];
        },

        setToStartOfDay = function(date)
        {
            if (isDate(date)) date.setHours(0,0,0,0);
        },

        compareDates = function(a,b)
        {
            // weak date comparison (use setToStartOfDay(date) to ensure correct result)
            return a.getTime() === b.getTime();
        },

        extend = function(to, from, overwrite)
        {
            var prop, hasProp;
            for (prop in from) {
                hasProp = to[prop] !== undefined;
                if (hasProp && typeof from[prop] === 'object' && from[prop].nodeName === undefined) {
                    if (isDate(from[prop])) {
                        if (overwrite) {
                            to[prop] = new Date(from[prop].getTime());
                        }
                    }
                    else if (isArray(from[prop])) {
                        if (overwrite) {
                            to[prop] = from[prop].slice(0);
                        }
                    } else {
                        to[prop] = extend({}, from[prop], overwrite);
                    }
                } else if (overwrite || !hasProp) {
                    to[prop] = from[prop];
                }
            }
            return to;
        },


        /**
        * defaults and localisation
        */
        defaults = {

            // bind the picker to a form field
            field: null,

            // automatically show/hide the picker on `field` focus (default `true` if `field` is set)
            bound: undefined,

            // the default output format for `.toString()` and `field` value
            format: 'YYYY-MM-DD',

            // the initial date to view when first opened
            defaultDate: null,

            // make the `defaultDate` the initial selected value
            setDefaultDate: false,

            // first day of week (0: Sunday, 1: Monday etc)
            firstDay: 0,

            // the minimum/earliest date that can be selected
            minDate: null,
            // the maximum/latest date that can be selected
            maxDate: null,

            // number of years either side, or array of upper/lower range
            yearRange: 10,

            // used internally (don't config outside)
            minYear: 0,
            maxYear: 9999,
            minMonth: undefined,
            maxMonth: undefined,

            isRTL: false,

            // how many months are visible (not implemented yet)
            numberOfMonths: 1,

            // internationalization
            i18n: {
                previousMonth : 'Previous Month',
                nextMonth     : 'Next Month',
                months        : ['January','February','March','April','May','June','July','August','September','October','November','December'],
                weekdays      : ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'],
                weekdaysShort : ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
            },

            // callback function
            onSelect: null,
            onOpen: null,
            onClose: null,
            onDraw: null
        },


        /**
        * templating functions to abstract HTML rendering
        */
        renderDayName = function(opts, day, abbr)
        {
            day += opts.firstDay;
            while (day >= 7) {
                day -= 7;
            }
            return abbr ? opts.i18n.weekdaysShort[day] : opts.i18n.weekdays[day];
        },

        renderDay = function(i, isSelected, isToday, isDisabled, isEmpty)
        {
            if (isEmpty) {
                return '<td class="is-empty"></td>';
            }
            var arr = [];
            if (isDisabled) {
                arr.push('is-disabled');
            }
            if (isToday) {
                arr.push('is-today');
            }
            if (isSelected) {
                arr.push('is-selected');
            }
            return '<td data-day="' + i + '" class="' + arr.join(' ') + '"><button class="pika-button" type="button">' + i + '</button>' + '</td>';
        },

        renderRow = function(days, isRTL)
        {
            return '<tr>' + (isRTL ? days.reverse() : days).join('') + '</tr>';
        },

        renderBody = function(rows)
        {
            return '<tbody>' + rows.join('') + '</tbody>';
        },

        renderHead = function(opts)
        {
            var i, arr = [];
            for (i = 0; i < 7; i++) {
                arr.push('<th scope="col"><abbr title="' + renderDayName(opts, i) + '">' + renderDayName(opts, i, true) + '</abbr></th>');
            }
            return '<thead>' + (opts.isRTL ? arr.reverse() : arr).join('') + '</thead>';
        },

        renderTitle = function(instance)
        {
            var i, j, arr,
                opts = instance._o,
                month = instance._m,
                year  = instance._y,
                isMinYear = year === opts.minYear,
                isMaxYear = year === opts.maxYear,
                html = '<div class="pika-title">',
                prev = true,
                next = true;

            for (arr = [], i = 0; i < 12; i++) {
                arr.push('<option value="' + i + '"' +
                    (i === month ? ' selected': '') +
                    ((isMinYear && i < opts.minMonth) || (isMaxYear && i > opts.maxMonth) ? 'disabled' : '') + '>' +
                    opts.i18n.months[i] + '</option>');
            }
            html += '<div class="pika-label">' + opts.i18n.months[month] + '<select class="pika-select pika-select-month">' + arr.join('') + '</select></div>';

            if (isArray(opts.yearRange)) {
                i = opts.yearRange[0];
                j = opts.yearRange[1] + 1;
            } else {
                i = year - opts.yearRange;
                j = 1 + year + opts.yearRange;
            }

            for (arr = []; i < j && i <= opts.maxYear; i++) {
                if (i >= opts.minYear) {
                    arr.push('<option value="' + i + '"' + (i === year ? ' selected': '') + '>' + (i) + '</option>');
                }
            }
            html += '<div class="pika-label">' + year + '<select class="pika-select pika-select-year">' + arr.join('') + '</select></div>';

            if (isMinYear && (month === 0 || opts.minMonth >= month)) {
                prev = false;
            }

            if (isMaxYear && (month === 11 || opts.maxMonth <= month)) {
                next = false;
            }

            html += '<button class="pika-prev' + (prev ? '' : ' is-disabled') + '" type="button">' + opts.i18n.previousMonth + '</button>';
            html += '<button class="pika-next' + (next ? '' : ' is-disabled') + '" type="button">' + opts.i18n.nextMonth + '</button>';

            return html += '</div>';
        },

        renderTable = function(opts, data)
        {
            return '<table cellpadding="0" cellspacing="0" class="pika-table">' + renderHead(opts) + renderBody(data) + '</table>';
        },


        /**
        * Pikaday constructor
        */
        Pikaday = function(options)
        {
            var self = this,
                opts = self.config(options);

            self._onMouseDown = function(e)
            {
                if (!self._v) {
                    return;
                }
                e = e || window.event;
                var target = e.target || e.srcElement;
                if (!target) {
                    return;
                }

                if (!hasClass(target, 'is-disabled')) {
                    if (hasClass(target, 'pika-button') && !hasClass(target, 'is-empty')) {
                        self.setDate(new Date(self._y, self._m, parseInt(target.innerHTML, 10)));
                        if (opts.bound) {
                            sto(function() {
                                self.hide();
                            }, 100);
                        }
                        return;
                    }
                    else if (hasClass(target, 'pika-prev')) {
                        self.prevMonth();
                    }
                    else if (hasClass(target, 'pika-next')) {
                        self.nextMonth();
                    }
                }
                if (!hasClass(target, 'pika-select')) {
                    if (e.preventDefault) {
                        e.preventDefault();
                    } else {
                        e.returnValue = false;
                        return false;
                    }
                } else {
                    self._c = true;
                }
            };

            self._onChange = function(e)
            {
                e = e || window.event;
                var target = e.target || e.srcElement;
                if (!target) {
                    return;
                }
                if (hasClass(target, 'pika-select-month')) {
                    self.gotoMonth(target.value);
                }
                else if (hasClass(target, 'pika-select-year')) {
                    self.gotoYear(target.value);
                }
            };

            self._onInputChange = function(e)
            {
                var date;

                if (e.firedBy === self) {
                    return;
                }
                if (hasMoment) {
                    date = moment(opts.field.value, opts.format);
                    date = (date && date.isValid()) ? date.toDate() : null;
                }
                else {
                    date = new Date(Date.parse(opts.field.value));
                }
                self.setDate(isDate(date) ? date : null);
                if (!self._v) {
                    self.show();
                }
            };

            self._onInputFocus = function()
            {
                self.show();
            };

            self._onInputClick = function()
            {
                self.show();
            };

            self._onInputBlur = function()
            {
                if (!self._c) {
                    self._b = sto(function() {
                        self.hide();
                    }, 50);
                }
                self._c = false;
            };

            self._onClick = function(e)
            {
                e = e || window.event;
                var target = e.target || e.srcElement,
                    pEl = target;
                if (!target) {
                    return;
                }
                if (!hasEventListeners && hasClass(target, 'pika-select')) {
                    if (!target.onchange) {
                        target.setAttribute('onchange', 'return;');
                        addEvent(target, 'change', self._onChange);
                    }
                }
                do {
                    if (hasClass(pEl, 'WCalendar')) {
                        return;
                    }
                }
                while ((pEl = pEl.parentNode));
                if (self._v && target !== opts.field) {
                    self.hide();
                }
            };

            self.el = document.createElement('div');
            self.el.className = 'WCalendar' + (opts.isRTL ? ' is-rtl' : '');

            addEvent(self.el, 'mousedown', self._onMouseDown, true);
            addEvent(self.el, 'change', self._onChange);

            if (opts.field) {
                if (opts.bound) {
                    document.body.appendChild(self.el);
                } else {
                    opts.field.parentNode.insertBefore(self.el, opts.field.nextSibling);
                }
                addEvent(opts.field, 'change', self._onInputChange);

                if (!opts.defaultDate) {
                    if (hasMoment && opts.field.value) {
                        opts.defaultDate = moment(opts.field.value, opts.format).toDate();
                    } else {
                        opts.defaultDate = new Date(Date.parse(opts.field.value));
                    }
                    opts.setDefaultDate = true;
                }
            }

            var defDate = opts.defaultDate;

            if (isDate(defDate)) {
                if (opts.setDefaultDate) {
                    self.setDate(defDate, true);
                } else {
                    self.gotoDate(defDate);
                }
            } else {
                self.gotoDate(new Date());
            }

            if (opts.bound) {
                this.hide();
                self.el.className += ' is-bound';
                addEvent(opts.field, 'click', self._onInputClick);
                addEvent(opts.field, 'focus', self._onInputFocus);
                addEvent(opts.field, 'blur', self._onInputBlur);
            } else {
                this.show();
            }

        };


        /**
        * public Pikaday API
        */
        Pikaday.prototype = {


            /**
            * configure functionality
            */
            config: function(options)
            {
                if (!this._o) {
                    this._o = extend({}, defaults, true);
                }

                var opts = extend(this._o, options, true);

                opts.isRTL = !!opts.isRTL;

                opts.field = (opts.field && opts.field.nodeName) ? opts.field : null;

                opts.bound = !!(opts.bound !== undefined ? opts.field && opts.bound : opts.field);

                var nom = parseInt(opts.numberOfMonths, 10) || 1;
                opts.numberOfMonths = nom > 4 ? 4 : nom;

                if (!isDate(opts.minDate)) {
                    opts.minDate = false;
                }
                if (!isDate(opts.maxDate)) {
                    opts.maxDate = false;
                }
                if ((opts.minDate && opts.maxDate) && opts.maxDate < opts.minDate) {
                    opts.maxDate = opts.minDate = false;
                }
                if (opts.minDate) {
                    setToStartOfDay(opts.minDate);
                    opts.minYear  = opts.minDate.getFullYear();
                    opts.minMonth = opts.minDate.getMonth();
                }
                if (opts.maxDate) {
                    setToStartOfDay(opts.maxDate);
                    opts.maxYear  = opts.maxDate.getFullYear();
                    opts.maxMonth = opts.maxDate.getMonth();
                }

                if (isArray(opts.yearRange)) {
                    var fallback = new Date().getFullYear() - 10;
                    opts.yearRange[0] = parseInt(opts.yearRange[0], 10) || fallback;
                    opts.yearRange[1] = parseInt(opts.yearRange[1], 10) || fallback;
                } else {
                    opts.yearRange = Math.abs(parseInt(opts.yearRange, 10)) || defaults.yearRange;
                    if (opts.yearRange > 100) {
                        opts.yearRange = 100;
                    }
                }

                return opts;
            },

            /**
            * return a formatted string of the current selection (using Moment.js if available)
            */
            toString: function(format)
            {
                var dd = this._d.getDate();
                var mm = this._d.getMonth() + 1;
                var yyyy = this._d.getFullYear();
                if(dd<10)
                {
                    dd = '0' + dd;
                }
                if(mm<10)
                {
                    mm = '0' + mm;
                }
                return !isDate(this._d) ? '' : mm + '/' + dd + '/' + yyyy;
            },

            /**
            * return a Moment.js object of the current selection (if available)
            */
            getMoment: function()
            {
                return hasMoment ? moment(this._d) : null;
            },

            /**
            * set the current selection from a Moment.js object (if available)
            */
            setMoment: function(date)
            {
                if (hasMoment && moment.isMoment(date)) {
                    this.setDate(date.toDate());
                }
            },

            /**
            * return a Date object of the current selection
            */
            getDate: function()
            {
                return isDate(this._d) ? new Date(this._d.getTime()) : null;
            },

            /**
            * set the current selection
            */
            setDate: function(date, preventOnSelect)
            {
                if (!date) {
                    this._d = null;
                    return this.draw();
                }
                if (typeof date === 'string') {
                    date = new Date(Date.parse(date));
                }
                if (!isDate(date)) {
                    return;
                }

                var min = this._o.minDate,
                    max = this._o.maxDate;

                if (isDate(min) && date < min) {
                    date = min;
                } else if (isDate(max) && date > max) {
                    date = max;
                }

                this._d = new Date(date.getTime());
                setToStartOfDay(this._d);
                this.gotoDate(this._d);

                if (this._o.field) {
                    this._o.field.value = this.toString();
                    fireEvent(this._o.field, 'change', { firedBy: this });
                }
                if (!preventOnSelect && typeof this._o.onSelect === 'function') {
                    this._o.onSelect.call(this, this.getDate());
                }
            },

            /**
            * change view to a specific date
            */
            gotoDate: function(date)
            {
                if (!isDate(date)) {
                    return;
                }
                this._y = date.getFullYear();
                this._m = date.getMonth();
                this.draw();
            },

            gotoToday: function()
            {
                this.gotoDate(new Date());
            },

            /**
            * change view to a specific month (zero-index, e.g. 0: January)
            */
            gotoMonth: function(month)
            {
                if (!isNaN( (month = parseInt(month, 10)) )) {
                    this._m = month < 0 ? 0 : month > 11 ? 11 : month;
                    this.draw();
                }
            },

            nextMonth: function()
            {
                if (++this._m > 11) {
                    this._m = 0;
                    this._y++;
                }
                this.draw();
            },

            prevMonth: function()
            {
                if (--this._m < 0) {
                    this._m = 11;
                    this._y--;
                }
                this.draw();
            },

            /**
            * change view to a specific full year (e.g. "2012")
            */
            gotoYear: function(year)
            {
                if (!isNaN(year)) {
                    this._y = parseInt(year, 10);
                    this.draw();
                }
            },

            /**
            * refresh the HTML
            */
            draw: function(force)
            {
                if (!this._v && !force) {
                    return;
                }
                var opts = this._o,
                    minYear = opts.minYear,
                    maxYear = opts.maxYear,
                    minMonth = opts.minMonth,
                    maxMonth = opts.maxMonth;

                if (this._y <= minYear) {
                    this._y = minYear;
                    if (!isNaN(minMonth) && this._m < minMonth) {
                        this._m = minMonth;
                    }
                }
                if (this._y >= maxYear) {
                    this._y = maxYear;
                    if (!isNaN(maxMonth) && this._m > maxMonth) {
                        this._m = maxMonth;
                    }
                }

                this.el.innerHTML = renderTitle(this) + this.render(this._y, this._m);

                if (opts.bound) {
                    var pEl  = opts.field,
                        left = pEl.offsetLeft,
                        top  = pEl.offsetTop + pEl.offsetHeight;
                    while((pEl = pEl.offsetParent)) {
                        left += pEl.offsetLeft;
                        top  += pEl.offsetTop;
                    }
                    this.el.style.cssText = 'position:absolute;left:' + left + 'px;top:' + top + 'px;';
                    sto(function() {
                        opts.field.focus();
                    }, 1);
                }

                if (typeof this._o.onDraw === 'function') {
                    var self = this;
                    sto(function() {
                        self._o.onDraw.call(self);
                    }, 0);
                }
            },

            /**
            * render HTML for a particular month
            */
            render: function(year, month)
            {
                var opts   = this._o,
                    now    = new Date(),
                    days   = getDaysInMonth(year, month),
                    before = new Date(year, month, 1).getDay(),
                    data   = [],
                    row    = [];
                setToStartOfDay(now);
                if (opts.firstDay > 0) {
                    before -= opts.firstDay;
                    if (before < 0) {
                        before += 7;
                    }
                }
                var cells = days + before,
                    after = cells;
                while(after > 7) {
                    after -= 7;
                }
                cells += 7 - after;
                for (var i = 0, r = 0; i < cells; i++)
                {
                    var day = new Date(year, month, 1 + (i - before)),
                        isDisabled = (opts.minDate && day < opts.minDate) || (opts.maxDate && day > opts.maxDate),
                        isSelected = isDate(this._d) ? compareDates(day, this._d) : false,
                        isToday = compareDates(day, now),
                        isEmpty = i < before || i >= (days + before);

                    row.push(renderDay(1 + (i - before), isSelected, isToday, isDisabled, isEmpty));

                    if (++r === 7) {
                        data.push(renderRow(row, opts.isRTL));
                        row = [];
                        r = 0;
                    }
                }
                return renderTable(opts, data);
            },

            isVisible: function()
            {
                return this._v;
            },

            show: function()
            {
                if (!this._v) {
                    if (this._o.bound) {
                        addEvent(document, 'click', this._onClick);
                    }
                    removeClass(this.el, 'is-hidden');
                    this._v = true;
                    this.draw();
                    if (typeof this._o.onOpen === 'function') {
                        this._o.onOpen.call(this);
                    }
                }
            },

            hide: function()
            {
                var v = this._v;
                if (v !== false) {
                    if (this._o.bound) {
                        removeEvent(document, 'click', this._onClick);
                    }
                    this.el.style.cssText = '';
                    addClass(this.el, 'is-hidden');
                    this._v = false;
                    if (v !== undefined && typeof this._o.onClose === 'function') {
                        this._o.onClose.call(this);
                    }
                }
            },

            /**
            * GAME OVER
            */
            destroy: function()
            {
                this.hide();
                removeEvent(this.el, 'mousedown', this._onMouseDown, true);
                removeEvent(this.el, 'change', this._onChange);
                if (this._o.field) {
                    removeEvent(this._o.field, 'change', this._onInputChange);
                    if (this._o.bound) {
                        removeEvent(this._o.field, 'click', this._onInputClick);
                        removeEvent(this._o.field, 'focus', this._onInputFocus);
                        removeEvent(this._o.field, 'blur', this._onInputBlur);
                    }
                }
                if (this.el.parentNode) {
                    this.el.parentNode.removeChild(this.el);
                }
            }

        };

        return Pikaday;

    }));

    WebElements.createCalendar = function(options)
    {
        var picker = new Pikaday(options);
        return picker;
    }
}

{
    (function(root) {
  /**
   * Namespace to hold all the code for timezone detection.
   */
  var jstz = (function () {
      'use strict';
      var HEMISPHERE_SOUTH = 's',

          /**
           * Gets the offset in minutes from UTC for a certain date.
           * @param {Date} date
           * @returns {Number}
           */
          get_date_offset = function (date) {
              var offset = -date.getTimezoneOffset();
              return (offset !== null ? offset : 0);
          },

          get_date = function (year, month, date) {
              var d = new Date();
              if (year !== undefined) {
                d.setFullYear(year);
              }
              d.setMonth(month);
              d.setDate(date);
              return d;
          },

          get_january_offset = function (year) {
              return get_date_offset(get_date(year, 0 ,2));
          },

          get_june_offset = function (year) {
              return get_date_offset(get_date(year, 5, 2));
          },

          /**
           * Private method.
           * Checks whether a given date is in daylight saving time.
           * If the date supplied is after august, we assume that we're checking
           * for southern hemisphere DST.
           * @param {Date} date
           * @returns {Boolean}
           */
          date_is_dst = function (date) {
              var is_southern = date.getMonth() > 7,
                  base_offset = is_southern ? get_june_offset(date.getFullYear()) :
                                              get_january_offset(date.getFullYear()),
                  date_offset = get_date_offset(date),
                  is_west = base_offset < 0,
                  dst_offset = base_offset - date_offset;

              if (!is_west && !is_southern) {
                  return dst_offset < 0;
              }

              return dst_offset !== 0;
          },

          /**
           * This function does some basic calculations to create information about
           * the user's timezone. It uses REFERENCE_YEAR as a solid year for which
           * the script has been tested rather than depend on the year set by the
           * client device.
           *
           * Returns a key that can be used to do lookups in jstz.olson.timezones.
           * eg: "720,1,2".
           *
           * @returns {String}
           */

          lookup_key = function () {
              var january_offset = get_january_offset(),
                  june_offset = get_june_offset(),
                  diff = january_offset - june_offset;

              if (diff < 0) {
                  return january_offset + ",1";
              } else if (diff > 0) {
                  return june_offset + ",1," + HEMISPHERE_SOUTH;
              }

              return january_offset + ",0";
          },

          /**
           * Uses get_timezone_info() to formulate a key to use in the olson.timezones dictionary.
           *
           * Returns a primitive object on the format:
           * {'timezone': TimeZone, 'key' : 'the key used to find the TimeZone object'}
           *
           * @returns Object
           */
          determine = function () {
              var key = lookup_key();
              return new jstz.TimeZone(jstz.olson.timezones[key]);
          },

          /**
           * This object contains information on when daylight savings starts for
           * different timezones.
           *
           * The list is short for a reason. Often we do not have to be very specific
           * to single out the correct timezone. But when we do, this list comes in
           * handy.
           *
           * Each value is a date denoting when daylight savings starts for that timezone.
           */
          dst_start_for = function (tz_name) {

            var ru_pre_dst_change = new Date(2010, 6, 15, 1, 0, 0, 0), // In 2010 Russia had DST, this allows us to detect Russia :)
                dst_starts = {
                    'America/Denver': new Date(2011, 2, 13, 3, 0, 0, 0),
                    'America/Mazatlan': new Date(2011, 3, 3, 3, 0, 0, 0),
                    'America/Chicago': new Date(2011, 2, 13, 3, 0, 0, 0),
                    'America/Mexico_City': new Date(2011, 3, 3, 3, 0, 0, 0),
                    'America/Asuncion': new Date(2012, 9, 7, 3, 0, 0, 0),
                    'America/Santiago': new Date(2012, 9, 3, 3, 0, 0, 0),
                    'America/Campo_Grande': new Date(2012, 9, 21, 5, 0, 0, 0),
                    'America/Montevideo': new Date(2011, 9, 2, 3, 0, 0, 0),
                    'America/Sao_Paulo': new Date(2011, 9, 16, 5, 0, 0, 0),
                    'America/Los_Angeles': new Date(2011, 2, 13, 8, 0, 0, 0),
                    'America/Santa_Isabel': new Date(2011, 3, 5, 8, 0, 0, 0),
                    'America/Havana': new Date(2012, 2, 10, 2, 0, 0, 0),
                    'America/New_York': new Date(2012, 2, 10, 7, 0, 0, 0),
                    'Europe/Helsinki': new Date(2013, 2, 31, 5, 0, 0, 0),
                    'Pacific/Auckland': new Date(2011, 8, 26, 7, 0, 0, 0),
                    'America/Halifax': new Date(2011, 2, 13, 6, 0, 0, 0),
                    'America/Goose_Bay': new Date(2011, 2, 13, 2, 1, 0, 0),
                    'America/Miquelon': new Date(2011, 2, 13, 5, 0, 0, 0),
                    'America/Godthab': new Date(2011, 2, 27, 1, 0, 0, 0),
                    'Europe/Moscow': ru_pre_dst_change,
                    'Asia/Amman': new Date(2013, 2, 29, 1, 0, 0, 0),
                    'Asia/Beirut': new Date(2013, 2, 31, 2, 0, 0, 0),
                    'Asia/Damascus': new Date(2013, 3, 6, 2, 0, 0, 0),
                    'Asia/Jerusalem': new Date(2013, 2, 29, 5, 0, 0, 0),
                    'Asia/Yekaterinburg': ru_pre_dst_change,
                    'Asia/Omsk': ru_pre_dst_change,
                    'Asia/Krasnoyarsk': ru_pre_dst_change,
                    'Asia/Irkutsk': ru_pre_dst_change,
                    'Asia/Yakutsk': ru_pre_dst_change,
                    'Asia/Vladivostok': ru_pre_dst_change,
                    'Asia/Baku': new Date(2013, 2, 31, 4, 0, 0),
                    'Asia/Yerevan': new Date(2013, 2, 31, 3, 0, 0),
                    'Asia/Kamchatka': ru_pre_dst_change,
                    'Asia/Gaza': new Date(2010, 2, 27, 4, 0, 0),
                    'Africa/Cairo': new Date(2010, 4, 1, 3, 0, 0),
                    'Europe/Minsk': ru_pre_dst_change,
                    'Pacific/Apia': new Date(2010, 10, 1, 1, 0, 0, 0),
                    'Pacific/Fiji': new Date(2010, 11, 1, 0, 0, 0),
                    'Australia/Perth': new Date(2008, 10, 1, 1, 0, 0, 0)
                };

              return dst_starts[tz_name];
          };

      return {
          determine: determine,
          date_is_dst: date_is_dst,
          dst_start_for: dst_start_for
      };
  }());

  /**
   * Simple object to perform ambiguity check and to return name of time zone.
   */
  jstz.TimeZone = function (tz_name) {
      'use strict';
        /**
         * The keys in this object are timezones that we know may be ambiguous after
         * a preliminary scan through the olson_tz object.
         *
         * The array of timezones to compare must be in the order that daylight savings
         * starts for the regions.
         */
      var AMBIGUITIES = {
              'America/Denver':       ['America/Denver', 'America/Mazatlan'],
              'America/Chicago':      ['America/Chicago', 'America/Mexico_City'],
              'America/Santiago':     ['America/Santiago', 'America/Asuncion', 'America/Campo_Grande'],
              'America/Montevideo':   ['America/Montevideo', 'America/Sao_Paulo'],
              'Asia/Beirut':          ['Asia/Amman', 'Asia/Jerusalem', 'Asia/Beirut', 'Europe/Helsinki','Asia/Damascus'],
              'Pacific/Auckland':     ['Pacific/Auckland', 'Pacific/Fiji'],
              'America/Los_Angeles':  ['America/Los_Angeles', 'America/Santa_Isabel'],
              'America/New_York':     ['America/Havana', 'America/New_York'],
              'America/Halifax':      ['America/Goose_Bay', 'America/Halifax'],
              'America/Godthab':      ['America/Miquelon', 'America/Godthab'],
              'Asia/Dubai':           ['Europe/Moscow'],
              'Asia/Dhaka':           ['Asia/Yekaterinburg'],
              'Asia/Jakarta':         ['Asia/Omsk'],
              'Asia/Shanghai':        ['Asia/Krasnoyarsk', 'Australia/Perth'],
              'Asia/Tokyo':           ['Asia/Irkutsk'],
              'Australia/Brisbane':   ['Asia/Yakutsk'],
              'Pacific/Noumea':       ['Asia/Vladivostok'],
              'Pacific/Tarawa':       ['Asia/Kamchatka', 'Pacific/Fiji'],
              'Pacific/Tongatapu':    ['Pacific/Apia'],
              'Asia/Baghdad':         ['Europe/Minsk'],
              'Asia/Baku':            ['Asia/Yerevan','Asia/Baku'],
              'Africa/Johannesburg':  ['Asia/Gaza', 'Africa/Cairo']
          },

          timezone_name = tz_name,

          /**
           * Checks if a timezone has possible ambiguities. I.e timezones that are similar.
           *
           * For example, if the preliminary scan determines that we're in America/Denver.
           * We double check here that we're really there and not in America/Mazatlan.
           *
           * This is done by checking known dates for when daylight savings start for different
           * timezones during 2010 and 2011.
           */
          ambiguity_check = function () {
              var ambiguity_list = AMBIGUITIES[timezone_name],
                  length = ambiguity_list.length,
                  i = 0,
                  tz = ambiguity_list[0];

              for (; i < length; i += 1) {
                  tz = ambiguity_list[i];

                  if (jstz.date_is_dst(jstz.dst_start_for(tz))) {
                      timezone_name = tz;
                      return;
                  }
              }
          },

          /**
           * Checks if it is possible that the timezone is ambiguous.
           */
          is_ambiguous = function () {
              return typeof (AMBIGUITIES[timezone_name]) !== 'undefined';
          };

      if (is_ambiguous()) {
          ambiguity_check();
      }

      return {
          name: function () {
              return timezone_name;
          }
      };
  };

  jstz.olson = {};

  /*
   * The keys in this dictionary are comma separated as such:
   *
   * First the offset compared to UTC time in minutes.
   *
   * Then a flag which is 0 if the timezone does not take daylight savings into account and 1 if it
   * does.
   *
   * Thirdly an optional 's' signifies that the timezone is in the southern hemisphere,
   * only interesting for timezones with DST.
   *
   * The mapped arrays is used for constructing the jstz.TimeZone object from within
   * jstz.determine_timezone();
   */
  jstz.olson.timezones = {
      '-720,0'   : 'Pacific/Majuro',
      '-660,0'   : 'Pacific/Pago_Pago',
      '-600,1'   : 'America/Adak',
      '-600,0'   : 'Pacific/Honolulu',
      '-570,0'   : 'Pacific/Marquesas',
      '-540,0'   : 'Pacific/Gambier',
      '-540,1'   : 'America/Anchorage',
      '-480,1'   : 'America/Los_Angeles',
      '-480,0'   : 'Pacific/Pitcairn',
      '-420,0'   : 'America/Phoenix',
      '-420,1'   : 'America/Denver',
      '-360,0'   : 'America/Guatemala',
      '-360,1'   : 'America/Chicago',
      '-360,1,s' : 'Pacific/Easter',
      '-300,0'   : 'America/Bogota',
      '-300,1'   : 'America/New_York',
      '-270,0'   : 'America/Caracas',
      '-240,1'   : 'America/Halifax',
      '-240,0'   : 'America/Santo_Domingo',
      '-240,1,s' : 'America/Santiago',
      '-210,1'   : 'America/St_Johns',
      '-180,1'   : 'America/Godthab',
      '-180,0'   : 'America/Argentina/Buenos_Aires',
      '-180,1,s' : 'America/Montevideo',
      '-120,0'   : 'America/Noronha',
      '-120,1'   : 'America/Noronha',
      '-60,1'    : 'Atlantic/Azores',
      '-60,0'    : 'Atlantic/Cape_Verde',
      '0,0'      : 'UTC',
      '0,1'      : 'Europe/London',
      '60,1'     : 'Europe/Berlin',
      '60,0'     : 'Africa/Lagos',
      '60,1,s'   : 'Africa/Windhoek',
      '120,1'    : 'Asia/Beirut',
      '120,0'    : 'Africa/Johannesburg',
      '180,0'    : 'Asia/Baghdad',
      '180,1'    : 'Europe/Moscow',
      '210,1'    : 'Asia/Tehran',
      '240,0'    : 'Asia/Dubai',
      '240,1'    : 'Asia/Baku',
      '270,0'    : 'Asia/Kabul',
      '300,1'    : 'Asia/Yekaterinburg',
      '300,0'    : 'Asia/Karachi',
      '330,0'    : 'Asia/Kolkata',
      '345,0'    : 'Asia/Kathmandu',
      '360,0'    : 'Asia/Dhaka',
      '360,1'    : 'Asia/Omsk',
      '390,0'    : 'Asia/Rangoon',
      '420,1'    : 'Asia/Krasnoyarsk',
      '420,0'    : 'Asia/Jakarta',
      '480,0'    : 'Asia/Shanghai',
      '480,1'    : 'Asia/Irkutsk',
      '525,0'    : 'Australia/Eucla',
      '525,1,s'  : 'Australia/Eucla',
      '540,1'    : 'Asia/Yakutsk',
      '540,0'    : 'Asia/Tokyo',
      '570,0'    : 'Australia/Darwin',
      '570,1,s'  : 'Australia/Adelaide',
      '600,0'    : 'Australia/Brisbane',
      '600,1'    : 'Asia/Vladivostok',
      '600,1,s'  : 'Australia/Sydney',
      '630,1,s'  : 'Australia/Lord_Howe',
      '660,1'    : 'Asia/Kamchatka',
      '660,0'    : 'Pacific/Noumea',
      '690,0'    : 'Pacific/Norfolk',
      '720,1,s'  : 'Pacific/Auckland',
      '720,0'    : 'Pacific/Tarawa',
      '765,1,s'  : 'Pacific/Chatham',
      '780,0'    : 'Pacific/Tongatapu',
      '780,1,s'  : 'Pacific/Apia',
      '840,0'    : 'Pacific/Kiritimati'
  };

  if (typeof exports !== 'undefined') {
    exports.jstz = jstz;
  } else {
    root.jstz = jstz;
  }
})(this);

    WebElements.timezone = function()
    {
        var tz = jstz.determine();
        return tz.name();
    }
}

WebElements.setCookie = function(name, value)
{
    document.cookie = name + "=" + value + ";"
}

WebElements.getCookie = function(name)
{
    currentcookie = document.cookie;
    if (currentcookie.length > 0)
    {
        firstidx = currentcookie.indexOf(name + "=");
        if (firstidx != -1)
        {
            firstidx = firstidx + name.length + 1;
            lastidx = currentcookie.indexOf(";",firstidx);
            if (lastidx == -1)
            {
                lastidx = currentcookie.length;
            }
            return unescape(currentcookie.substring(firstidx, lastidx));
        }
    }
    return "";
}

WebElements.openAccordion = function(content, image, value)
{
    var content = WebElements.get(content);
    var image = WebElements.get(image);
    var value = WebElements.get(value);

    WebElements.show(content);
    value.value = 'True';
    image.src = WebElements.Settings.hideImage;
}

WebElements.closeAccordion = function(content, image, value)
{
    var content = WebElements.get(content);
    var image = WebElements.get(image);
    var value = WebElements.get(value);

    WebElements.hide(content);
    value.value = 'False';
    image.src =  WebElements.Settings.showImage;
}

WebElements.toggleAccordion = function(content, image, value)
{
    if(!WebElements.shown(content))
    {
        WebElements.openAccordion(content, image, value);
    }
    else
    {
        WebElements.closeAccordion(content, image, value);
    }
}
