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

//Provide basic platform information under Platform name-space
var Platform = Platform || {}
Platform.IS_IOS = /Apple.*Mobile/.test(navigator.userAgent)
Platform.IS_OPERA = Object.prototype.toString.call(window.opera) == '[object Opera]';
Platform.IS_IE = navigator.appVersion.match(/\bMSIE\b/) && !!window.attachEvent && !Platform.IS_OPERA;
Platform.IS_WEBKIT = navigator.userAgent.indexOf('AppleWebKit/') > -1
Platform.IS_GECKO = navigator.userAgent.indexOf('Gecko') > -1 && navigator.userAgent.indexOf('KHTML') === -1

//Create main WebElement name space - pulling in Keys and Platform name space's
var WebElements = WebElements || {}
WebElements.Keys = Keys;
WebElements.Platform = Platform;

WebElements.Settings = {}
WebElements.Settings.throbberImage = 'images/throbber.gif';
WebElements.Settings.Serialize = ['input', 'textarea', 'select'];

WebElements.State = {}
WebElements.State.dropDownOpen = false;
WebElements.State.currentDropDown = null;
WebElements.State.currentButton = null;

//Returns the element given (if it is a page element) or the result of getElementId
WebElements.get = function (element)
{
    //If an actual element is given (or nothing is given) just return it
    if(!element || element.innerHTML != null || element == document)
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
        newArray.push(arrayOfItems[currentItem]);
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
    var elements = parentNode;
    if(!parentNode instanceof Array)
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
    return throbber;
}

//Gets elements by there css class that are childern of a certain node - uses native implementation if present
WebElements.getElementsByClassName = function(className, parentNode, stopOnFirstMatch)
{
    parentNode = WebElements.get(parentNode);
    if(document.getElementByClassName){
        if(parentNode)
        {
            return parentNode.getElementByClassName(className);
        }
        else
        {
            return document.getElementByClassName(className);
        }
    }
    if(!parentNode)
    {
        parentNode = document.getElementsByTagName("body")[0];
    }

    var regexp = new RegExp('\\b' + className + '\\b');
    return WebElements.getByCondition(function(element){regexp.test(element.className)}, parentNode, stopOnFirstMatch);
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
    element.style.left = WebElements.plixelsToLeft(parentElement) + pixelsToRight;
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
    WebElements.showElement(dropDownElement);
}

//Toggles the displayed state of a drop down menu
WebElements.toggleDropDown = function(dropDown, parentElement)
{
    var dropDown = WebElements.get(dropDown);
    WebElements.shown(dropDown) && WebElements.hide(dropDown) || WebElements.displayDropDown(dropDown, parentElement);
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

//Get first child element (exluding empty elements)
WebElements.firstChild = function(element)
{
    var element = WebElements.get(element);
    if(element.firstChild)
    {
        element = element.firstChild
    }
    while ((!element || element.innerHTML == null) && element.nextSibling)
    {
        element = element.nextSibling;
    }
    return element;
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

//Forces this to be the only peer with class
WebElements.stealClassFromPeer = function(element, className)
{
    WebElements.forEach(WebElements.peer(element, className),
                                         function(element){WebElements.removeClass(element, className)});
    WebElements.addClass(element, className);
}

//Forces this to be the only peer with class
WebElements.stealClassFromFellowChild = function(element, parentClassName, className)
{
    var fellowChild = WebElements.fellowChild(element, parentClassName, className);
    if(fellowChild)
    {
        WebElements.removeClass(fellowChild, className);
    }
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
    if(WebElements.get(element).style.display == "none")
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
WebElements.move = function(element, to)
{
    WebElements.get(to).appendChild(WebElements.get(element));
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
        WebElements.removeClass(WebElements.State.currentButton, 'SelectedDropDown');
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

// attaches html5 drag and drop file uploading capabilities to an drop down skeleton
WebElements.buildFileOpener = function(dropBox)
{
    var dropBox = WebElements.get(dropBox);
    var statusBar = WebElements.get(dropBox.id + 'StatusBar');
    var dropLabel = WebElements.get(dropBox.id + 'DropLabel');
    var fileTemplate = WebElements.get(dropBox.id + 'File');
    var filesContainer = WebElements.get(dropBox.id + 'Files');

    // init event handlers
    dropBox.addEventListener("dragenter", WebElements.stopOperation, false);
    dropBox.addEventListener("dragexit", WebElements.stopOperation, false);
    dropBox.addEventListener("dragover", WebElements.stopOperation, false);
    dropBox.addEventListener("drop", function(evt){
        evt.preventDefault(evt);

        var files = evt.dataTransfer.files;
        var count = files.length;

        // Only call the handler if 1 or more files was dropped.
        if (files.length > 0)
        {
            WebElements.show(statusBar);
            WebElements.removeClass(dropBox, "WEmpty");
            WebElements.forEach(files, function(file){
                dropLabel.innerHTML = "Processing " + file.name;

                var reader = new FileReader();
                reader.file = file;

                // init the reader event handlers
                reader.onload = function(evt)
                {
                    var fileName = dropBox.id + evt.target.file.name;
                     if(WebElements.get(fileName))
                     {
                         return; // Don't upload the same file twice but don't annoy users with pesky errors
                     }
                    newFile = WebElements.copy(fileTemplate, filesContainer, false);
                    alert("OO")
                    newFile.id = fileName;
                    WebElements.show(newFile);
                    WebElements.getElementByClassName('WThumbnail', newFile).src = evt.target.result;
                    WebElements.getElementByClassName('WFileName', newFile).innerHTML = evt.target.file.name;
                };

                // begin the read operation
                reader.readAsDataURL(file);
            });
        }
        WebElements.hide(statusBar);

    }, false);
}

WebElements.clickDropDown = function(menu, openOnly, button, parentElement)
{
    WebElements.State.dropDownOpen = true;
    if(WebElements.State.currentDropDown && WebElements.State.currentDropDown != menu)
    {
        WebElements.hide(currentDropDown);
        WebElements.removeClass(currentButton, 'SelectedDropDown');
    }
    WebElements.State.currentDropDown = menu;
    WebElements.State.currentButton = button;
    if(!openOnly || !WebElements.shown(currentDropDown)){
        if(WebElements.toggleDropDown(currentDropDown, parentElement)){
            WebElements.addClass(button, 'SelectedDropDown');
        }
        else{
            WebElements.removeClass(button, 'SelectedDropDown');
       }
   }
}


//attach on click event to body to close any open pop up menus when a random click is placed
WebElements.State.oldDocumentOnload = document.onload;
document.onload = function()
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
    if(WebElements.State.oldDocumentOnload)
    {
        WebElements.State.oldDocumentOnload();
    }
}

WebElements.serialize = function(field)
{
    var element = WebElements.get(field);
    var tagName = element.tagName.toLowerCase();
    var key = encodeURIComponent(element.name);
    if(!key)
    {
        return '';
    }
    if(tagName == "input" || tagName == "textArea")
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
    if(window.confirm('%s'))
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
