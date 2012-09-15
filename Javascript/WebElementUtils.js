/* Javascript Utils
 *
 * Contains general functions which ease the usage of multi-browser Javascript coding
 * and are unrelated to Prototype, or other javascript libraries.
 *
 */

var TAB = 9;
var ENTER = 13;
var DOWN_ARROW = 40;
var IS_IOS = navigator.platform == 'iPad' || navigator.platform == 'iPhone' || navigator.platform == 'iPod'

var currentDropDown = null;
var currentButton = null;
var throbberImage = 'images/throbber.gif';

//returns the element given (if it is a page element) or the result of getElementId
function WEGetElement(element)
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

function WEGetValue(element)
{
    var element = WEGetElement(element)
    if (element)
    {
        return element.value;
    }

    return ""
}

//Hides Elements with a particular class name
function WEHideClass(className, parentNode)
{
    var elements = WEGetElementsByClassName(className, parentNode);
    for(var currentElement=0; currentElement < elements.length; currentElement++)
    {
        var element = elements[currentElement];
        WEHideElement(element)
    }
}

//Shows Elements with a particular class name
function WEShowClass(className, parentNode)
{
    var elements = WEGetElementsByClassName(className, parentNode);
    for(var currentElement=0; currentElement < elements.length; currentElement++)
    {
        var element = elements[currentElement];
        WEShowElement(element);
    }
}


//Creates a throbber on the fly, change window.throbberImage to edit image
function WEBuildThrobber()
{
    var throbber = document.createElement('img');
    throbber.src = throbberImage;
    return throbber;
}

//Gets elements by there css class that are childern of a certain node
function WEGetElementsByClassName(classname, parentNode)
{
    parentNode = WEGetElement(parentNode);
    if(document.getElementByClassName){
        if(parentNode)
        {
            parentNode.getElementByClassName(className);
        }
        else
        {
            document.getElementByClassName(className);
        }
    }

    if(!parentNode)
    {
        if(document.getElementsByClassName)
        {
            return document.getElementsByClassName(classname);
        }
        else
        {
            parentNode = document.getElementsByTagName("body")[0];
        }
    }
    else
    {
        parentNode = WEGetElement(parentNode);
    }

    var elements_to_return = [];
    var regexp = new RegExp('\\b' + classname + '\\b');
    var elements = parentNode.getElementsByTagName("*");

    for(var currentElement=0; currentElement < elements.length; currentElement++)
    {
        element = elements[currentElement];
        if(regexp.test(element.className))
        {
            elements_to_return.push(element);
        }
    }

    return elements_to_return;
}

//Returns elements that pass a conditional callback
function WEGetElementsByCondition(conditional, parentNode)
{
    var parentNode = WEGetElement(parentNode);
    var elements_to_return = [];
    var elements = parentNode.getElementsByTagName("*");

    for(var currentElement=0; currentElement < elements.length; currentElement++)
    {
        element = elements[currentElement];
        if(conditional(element))
        {
            elements_to_return.push(element);
        }
    }

    return elements_to_return;
}

//Returns children of an element by their name
function WEGetChildrenByName(parentNode, name)
{
    return WEGetElementsByCondition(function(element){return element.name == name}, parentNode);
}

//Returns a child of an element by its name
function WEGetChildByName(parentNode, name)
{
    return WEGetChildrenByName(parentNode, name)[0];
}


//populates a form using an id/name:value dictionary -- such as a request dictionary.
function WEPopulate(fieldDict)
{
    for(fieldId in fieldDict)
    {
        field = WEGetElement(fieldId);
        value = fieldDict[fieldId];
        if(field && value)
        {
            field.value = value;
        }
    }
}

//updates a countdown label slowly deincrementing till reaches 0 than calls action
function WECountDown(label, seconds, action)
{
    var label = WEGetElement(label);
    label.innerHTML = seconds;
    label.timeoutList = []

    for(var currentCount = 1; currentCount < seconds; currentCount++)
    {
        timeout = setTimeout('WEGetElement(\'' + label.id + '\').innerHTML = ' +
                  (seconds - currentCount) + ';', (currentCount * 1000));
        label.timeoutList.push(timeout);
    }

    timeout = setTimeout('WEGetElement(\'' + label.id + '\').innerHTML = 0;' +
                         action, seconds * 1000);
    label.timeoutList.push(timeout);
}

//updates a countdown label slowly deincrementing till reaches 0 than calls action
function WEAbortCountDown(label)
{
    var label = WEGetElement(label);
    var timeoutList = label.timeoutList

    for(var currentTimeout = 0; currentTimeout < timeoutList.length; currentTimeout++)
    {
        var timeout = timeoutList[currentTimeout];
        clearTimeout(timeout);
    }
}

//Returns the number of pixels left of element
function WEPixelsToLeft(element)
{
    var aTag = WEGetElement(element);

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
function WEPixelsAbove(element)
{
    var aTag = WEGetElement(element);

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
function WESetAbsoluteRelativeToParent(element, pixelsDown, pixelsToRight, parentElement)
{
    var element = WEGetElement(element);
    if(parentElement == null)
    {
        parentElement = element.parentNode;
    }
    else
    {
        parentElement = WEGetElement(parentElement);
    }
    if(pixelsDown == null)
    {
        pixelsDown = 0;
    }
    if(pixelsToRight == null)
    {
        pixelsToRight = 0;
    }

    element.style.left = WEPixelsToLeft(parentElement) + pixelsToRight;
    element.style.top = WEPixelsAbove(parentElement) + pixelsDown;
}

//Sets an element position to that of its parents + pixelsDown & pixelsToRight
function WEDisplayDropDown(dropDown, parentElement)
{
    var dropDownElement = WEGetElement(dropDown);
    if(parentElement == null)
    {
        parentElement = dropDownElement.parentNode;
    }
    else
    {
        parentElement = WEGetElement(parentElement);
    }

    WESetAbsoluteRelativeToParent(dropDownElement, parentElement.offsetHeight -1,
                                  0, parentElement);
    WEShowElement(dropDownElement);
}

function WEToggleDropDown(dropDown, parentElement)
{
    if(WEElementShown(dropDown))
    {
        WEHideElement(dropDown);
        return false;
    }
    else
    {
        WEDisplayDropDown(dropDown, parentElement);
        return true;
    }
}

//Gets the first element in parent node with a certain class name
function WEGetElementByClassName(classname, parentNode)
{
    var elements = WEGetElementsByClassName(classname, parentNode);
    if(elements.length > 0)
    {
        return elements[0];
    }
    else
    {
        return null;
    }
}
function WEOpenAccordion(accordionName)
{
    var elementContent = WEGetElementByClassName('AccordionContent', accordionName);
    var elementValue = WEGetElement(accordionName + 'Value');
    var elementImage = WEGetElement(accordionName + 'Image');
    WEShowElement(elementContent);
    elementValue.value = 'True';
    elementImage.src = 'images/hide.gif';
}


function WEFellowChild(element, parentClass, childClass)
{
    return WEGetElementByClassName(childClass, WEParentElement(element, parentClass));
}

//Get first child element (exluding empty elements)
function WEFirstChildElement(element)
{
    var element = WEGetElement(element);
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

//Get first child element (exluding empty elements)
function WELastChildElement(element)
{
    var element = WEGetElement(element);
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


//Same as element.nextSibling except it is called
//as WENextElement(object) and ignores blank elements
function WENextElement(element)
{
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

//increments the value of a hiddenField
function WEIncrement(element, max)
{
    var element = WEGetElement(element);
    var number = parseInt(element.value)
    if(!number){
        number = 0;
    }
    number += 1;
    if(max != undefined && number > max){
        number = max;
    }
    element.value = number;
    if(element.onchange)
    {
        element.onchange();
    }
}

//deincrements the value of a hiddenField
function WEDeincrement(element, min)
{
    var element = WEGetElement(element);
    var number = parseInt(element.value)
    if(!number){
        number = 0;
    }
    number -= 1;
    if(min != undefined && number < min){
        number = min;
    }
    element.value = number;
    element.onchange();
}

//Sets the prefix for the container and all childElements
function WESetPrefix(container, prefix)
{
    var container = WEGetElement(container);
    container.id = prefix + container.id;
    container.name = prefix + container.name;

    var children = WEChildElements(container);
    for(currentChild = 0; currentChild != children.length; currentChild++)
    {
        var child = children[currentChild];
        child.id = prefix + child.id;
        child.name = prefix + child.name;
    }

}

//Same as element.previousSibling except it is called
//as WEPrevElement(object) and ignores blank elements
function WEPrevElement(element)
{
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

//Same as element.parentNode except it is called as
//WEParentElement(object) and ignores blank elements
function WEParentElement(element, className, giveUpAtClass)
{
    var element = WEGetElement(element);
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
function WEClearChildren(element, replacement)
{
    var childElements = WEChildElements(element);
    if(childElements)
    {
        for(var currentChild = 0; currentChild < childElements.length; currentChild++)
        {
            WERemoveElement(childElements[currentChild]);
        }
    }
    if(replacement)
    {
        element.appendChild(replacement)
    }
}

//Allows you to get a childElement by class name
function WEChildElement(element, className)
{
    var element = WEGetElement(element);
    return WEGetElementByClassName(className, element);
}

//Allows you to get childElements by class name if provided or simply returns all child elements
function WEChildElements(parentElement, className)
{
    var parentElement = WEGetElement(parentElement);
    if(className != null)
    {
        return WEGetElementsByClassName(className, parentElement);
    }

    var childElements = parentElement.getElementsByTagName('*');
    var returnedChildren = Array();
    for(var currentChild = 0; currentChild != childElements.length; currentChild++)
    {
        var child = childElements[currentChild];
        if(child && child.innerHTML != null)
        {
            returnedChildren.push(child);
        }
    }

    return returnedChildren;
}



//Allows you to get an element in the same location on the tree based on a classname
function WEPeer(element, className)
{
    var parentElement = WEGetElement(element).parentNode
    return WEChildElement(parentElement, className);
}

//Forces this to be the only peer with class
function WEStealClassFromPeer(element, className)
{
    var peer = WEPeer(element, className);
    if(peer)
    {
        WERemoveClass(peer, className);
    }
    WEAddClass(element, className);
}

//Forces this to be the only peer with class
function WEStealClassFromFellowChild(element, parentClassName, className)
{
    var fellowChild = WEFellowChild(element, parentClassName, className);
    if(fellowChild)
    {
        WERemoveClass(fellowChild, className);
    }
    WEAddClass(element, className);
}

//hides an element by setting its display property to none
function WEHideElement(element)
{
    var element = WEGetElement(element);
    if(element != null)
    {
        element.style.display = "none";
        return true;
    }
    return false;
}

//shows an element by setting its display property to block
function WEShowElement(element)
{
    var element = WEGetElement(element);
    if(element != null)
    {
        var tagName = element.tagName.toLowerCase();
        if(tagName == "span")
        {
            element.style.display = "inline";
        }
        else if(tagName == "tr")
        {
            element.style.display = "";
        }
        else
        {
            element.style.display = "block";
        }
        return true;
    }
    return false;
}

//shows the element if it is hidden - hides it if it is visable
function WEToggleElement(element)
{
    if(WEElementShown(element))
    {
        WEHideElement(element);
        return true;
    }
    WEShowElement(element);
    return false;
}

//return if the element is visable or not
function WEElementShown(element)
{
    var element = WEGetElement(element);
    if(element.style.display == "none")
    {
        return false;
    }
    return true;
}

//replaces 'element' with 'newElement' (element must contain a parent element)
function WEReplaceElement(element, newElement)
{
   var element = WEGetElement(element);
   var elementParent = element.parentNode;
   if(!elementParent)
   {
       return false;
   }

   var newElement = WEGetElement(newElement);
   elementParent.replaceChild(newElement, element);
   return true;
}

//removes 'element' from the page (element must contain a parent element)
function WERemoveElement(element)
{
    var element = WEGetElement(element);
    var elementParent = element.parentNode;
    if(!elementParent)
    {
        return false;
    }

    elementParent.removeChild(element);
    return true;
}

//clears the innerHTML of an element
function WEClear(element)
{
    var element = WEGetElement(element);
    element.innerHTML = "";
}

//adds an option to a selectbox with a specified name and value
function WEAddOption(selectElement, optionName, optionValue)
{
    var selectElement = WEGetElement(selectElement);
    if(optionValue == undefined){
        optionValue = optionName;
    }
    newOption = document.createElement('option');
    newOption.innerHTML = optionName;
    newOption.value = optionValue;
    selectElement.appendChild(newOption);
}

//adds html to element
function WEAddHtml(element, html)
{
    var element = WEGetElement(element);
    var newDiv = document.createElement('div');
    newDiv.innerHTML = html;
    element.appendChild(newDiv);
    return newDiv
}

//moves a div
function WEMove(element, to)
{
    var element = WEGetElement(element);
    var to = WEGetElement(to);
    to.appendChild(element);
}

//makes a copy of an element into 'to' incrementing its id and returns the copy
function WECopy(element, to, incrementId)
{
    if(incrementId == null){incrementId = true;}

    var element = WEGetElement(element);
    var to = WEGetElement(to);

    var elementCopy = element.cloneNode(true);
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
    to.appendChild(elementCopy);

    if(incrementId)
    {
        elementCopy.innerHTML = WEReplaceAll(html, toReplace, replacement);
    }

    return elementCopy
}

//returns true if text WEContains subtext false if not
function WEContains(text, subtext, caseSensitive)
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

//returns true if any words within text start with subtext
function WEStartsWith(text, subtext, caseSensitive)
{
    if(!caseSensitive)
    {
        var text = text.toLowerCase();
        var subtext = subtext.toLowerCase();
    }

    var text = WEReplaceAll(text, ">", " ");
    text = WEReplaceAll(text, "<", " ");
    text = WEReplaceAll(text, ",", " ");
    text = WEReplaceAll(text, "|", " ");
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
function WEAddPrefix(container, prefix)
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


//perform the javascript contained on the page --
//contained in elements innerHTML where the
//class is set to 'onLoadJavascript'
//made for use on AJAX pages -- inflicts a noticable performance penalty over <script>
function WEDoInPageJavascript(container)
{
    var container = WEGetElement(container);
    var elements = WEGetElementsByClassName("onLoadJavascript", container);
    for(currentElement = 0; currentElement < elements.length; currentElement++)
    {
        var element = elements[currentElement]
        if(element.innerHTML != null && element.innerHTML != "")
        {
            scriptTag = document.createElement('script');
            scriptTag.type = "text/javascript"
            container.appendChild(scriptTag)

            scriptTag.text = WEUnserialize(element.innerHTML);
        }
    }
}

function WEUnserialize(html)
{
    var html = String(html);
    html = WEReplaceAll(html, "&lt;", "<");
    html = WEReplaceAll(html, "&gt;", ">");
    html = WEReplaceAll(html, "&amp;", "&");
    return html
}

//sorts a list alphabetically by innerHTML
function WESortSelect(selectElement)
{
    var selectElement = WEGetElement(selectElement);
    var selectOptions = selectElement.options;
    var sorted = new Array();
    var selectElementSorted = new Array();

    for(var currentOption = 0; currentOption < selectOptions.length; currentOption++)
    {
        var option = selectOptions[currentOption];
        sorted[currentOption] = new Array();
        sorted[currentOption][0] = option.innerHTML;
        sorted[currentOption][1] = option.value;
        sorted[currentOption][2] = option.id;
    }

    sorted.sort();
    for(var currentOption=0; currentOption < sorted.length; currentOption++)
    {
        selectElement.options[currentOption].innerHTML=sorted[currentOption][0];
        selectElement.options[currentOption].value=sorted[currentOption][1];
        selectElement.options[currentOption].id = sorted[currentOption][2];
    }
}

//sorts a list by value
function WESortSelectByValue(selectElement)
{
    var selectElement = WEGetElement(selectElement);
    var selectOptions = selectElement.options;
    var sorted = new Array();
    var selectElementSorted = new Array();

    for(var currentOption = 0; currentOption < selectOptions.length; currentOption++)
    {
        var option = selectOptions[currentOption];
        sorted[currentOption] = new Array();
        sorted[currentOption][0] = option.value;
        sorted[currentOption][1] = option.innerHTML;
        sorted[currentOption][2] = option.id;
        sorted[currentOption][3] = option.disabled;
    }

    sorted.sort();

    for(var currentOption=0; currentOption < sorted.length; currentOption++)
    {
        selectElement.options[currentOption].value=sorted[currentOption][0];
        selectElement.options[currentOption].innerHTML=sorted[currentOption][1];
        selectElement.options[currentOption].id = sorted[currentOption][2];
        selectElement.options[currentOption].disabled = sorted[currentOption][3];
    }
}

//returns a list without duplicate elements
function WERemoveDuplicates(inArray)
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
function WESelectedOptions(selectBox)
{
    var selectBox = WEGetElement(selectBox);
    var options = selectBox.options;

    var selectedOptions = Array();
    for(currentOption = 0; currentOption < options.length; currentOption++)
    {
        var option = options[currentOption];
        if (option.selected)
        {
            selectedOptions.push(option)
        }
    }
    return selectedOptions
}

//Selects all element of a select box
function WESelectAllOptions(selectBox)
{
    var selectBox = WEGetElement(selectBox);
    var options = selectBox.options;

    var selectedOptions = Array();
    for(currentOption = 0; currentOption < options.length; currentOption++)
    {
        var option = options[currentOption];
        option.selected = true;
    }
}

//returns the selected checkboxes withing a container
function WESelectedCheckboxes(container)
{
    var container = WEGetElement(container);
    var elements = WEChildElements(container);

    var selectedCheckboxes = Array();
    for(currentElement = 0; currentElement < elements.length; currentElement++)
    {
        var element = elements[currentElement];
        if (element.checked)
        {
            selectedCheckboxes.push(element.name)
        }
    }
    return selectedCheckboxes
}

function WESelectAllCheckboxes(container, check)
{
    if(check == null){var check = true;}

    var children = WEChildElements(container);
    for(current = 0; current < children.length; current++)
    {
        var child = children[current];
        if(child.type == 'checkbox')
        {
            child.checked = check;
        }
    }
}

//returns all nested values within a contianer
function WEGetValues(container, checkSelected, tagName)
{
    if(checkSelected == null){var checkSelected = false;}
    if(!tagName) { tagName = "option"; }

    var container = WEGetElement(container);
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
function WEGetElementByValue(element, value)
{
    var element = WEGetElement(element);

    var children = WEChildElements(element);
    for(current = 0; current < children.length; current++)
    {
        var child = children[current];
        if(child.value == value)
        {
            return child;
        }
    }

    return false;
}

//Get a child element of element based on innerHtml
function WEGetElementByInnerHTML(element, text)
{
    var element = WEGetElement(element);

    var children = WEChildElements(element);
    for(current = 0; current < children.length; current++)
    {
        var child = children[current];
        if(child.innerHTML == text)
        {
            return child;
        }
    }

    return false;
}

//returns the first selected option within a select box
function WESelectedOption(selectBox)
{
    var selectBox = WEGetElement(selectBox);
    var options = selectBox.options;

    for(currentOption = 0; currentOption < options.length; currentOption++)
    {
        var option = options[currentOption];
        if (option.selected)
        {
            return option;
        }
    }

    return null
}

//selects an element based on its value
function WESelectOption(selectBox, option)
{
    WESelectedOption(selectBox).selected = false;
    WEGetElementByValue(selectBox, option).selected = true;
}

//replaces all instances of a string with another string
function WEReplaceAll(string, toReplace, replacement)
{
    return string.split(toReplace).join(replacement);
}

//returns all css classes attached to an element as a list
function WEClasses(element)
{
    var element = WEGetElement(element);
    if(!element)
    {
        return [];
    }
    var classes = element.className;
    return classes.split(" ");
}

//returns true if element contains class
function WEHasClass(element, className)
{
    var element = WEGetElement(element)
    var regexp = new RegExp('\\b' + className + '\\b');
    if(regexp.test(element.className))
    {
        return true;
    }
    return false;
}

//sets an elements classes based on the passed in list
function WESetClasses(element, classList)
{
    var element = WEGetElement(element);
    element.className = classList.join(" ");
}

//removes a css class
function WERemoveClass(element, classToRemove)
{
    WESetClasses(element, WERemoveFromArray(WEClasses(element), classToRemove))
}

//adds a css class
function WEAddClass(element, classToAdd)
{
    var element = WEGetElement(element);
    var styleClasses = WEClasses(element);

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

function WERemoveFromArray(existingArray, toRemove)
{
    newArrayToReturn = [];
    for(currentIndex = 0; currentIndex < existingArray.length; currentIndex++)
    {
        currentItem = existingArray[currentIndex];
        if(currentItem != toRemove)
        {
            newArrayToReturn.push(currentItem);
        }
    }
    return newArrayToReturn;
}

//lets you choose one class out of a list of class choices
function WEChooseClass(element, classes, choice)
{
    var element = WEGetElement(element);
    var styleClasses = WEClasses(element);
    for(currentClass = 0; currentClass < classes.length; currentClass++){
        styleClasses = WERemoveFromArray(styleClasses, classes[currentClass]);
    }
    styleClasses.push(choice);
    WESetClasses(element, styleClasses);
}

//forces the browser to redraw the element (Needs to exist becuase IE is Evil)
function WERedraw(element)
{
    var element = WEGetElement(element);
    var parentElement = element.parentNode;
    var html = parentElement.innerHTML;

    parentElement.innerHTML = "";
    parentElement.innerHTML = html;
}

//Simple way to access data within div section
function WEAttribute(element, attribute)
{
    element = WEGetElementByClassName(attribute + "Value", element)
    if(element == null)
    {
        return "";
    }

    if(element.nodeName.toLowerCase() == "input")
    {
        return element.value;
    }
    else
    {
        return WEStrip(element.innerHTML);
    }
}

//Simple way to set an attribute in a div section
function WESetAttribute(element, attribute, value)
{
    element = WEChildElement(element, attribute + "Value")
    if(element == null)
    {
        return false;
    }

    if(element.nodeName.toLowerCase() == "input")
    {
        element.value = value;
        if(element.onchange)
        {
            element.onchange()
        }
    }
    else
    {
        element.innerHTML = value;
    }
    return true;
}


//Simple way to export variables within a div
function WEExport(element, delimiter, max)
{
    if(delimiter == null)
    {
        delimiter = ","
    }

    var exportedValue = [];
    var values = WEGetElementsByClassName("Value", element);
    for(currentValue = 0; currentValue < values.length; currentValue++)
    {
        element = values[currentValue];
        if(max == currentValue)
        {
            break;
        }
        if(element.nodeName.toLowerCase() == "input")
        {
            exportedValue.push(WEStrip(element.value));
        }
        else
        {
            exportedValue.push(WEStrip(element.innerHTML));
        }
    }
    return exportedValue.join(delimiter);
}

//Strip spaces before and after string
function WEStrip(string)
{
    return string.replace(/^\s+|\s+$/g,"");
}

//Easy way to see if a value is contained in a list
function WEInList(list, value)
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
function WEAppendOnce(list, listItem)
{
    if(!WEInList(list, listItem))
    {
        list.push(listItem)
    }
}

//Combines two lists into one ignoring duplicate values
function WECombine(list, list2)
{
    for(var currentListItem = 0; currentListItem < list2.length; currentListItem++)
    {
        listItem = list2[currentListItem];
        WEAppendOnce(list, listItem);
    }
}

//suppress a single nodes onclick event
function WESuppress(element, attribute)
{
    var element = WEGetElement(element);

    element['suppressed_' + attribute] = element[attribute];
    element[attribute] = null;
}

//unsuppress the supressed javascript event
function WEUnsuppress(element, attribute)
{
    var element = WEGetElement(element);

    element[attribute] = element['suppressed_' + attribute];
    element['suppressed_' + attribute] = element[attribute];
}

function WEToggleMenu(button)
{
    var menu = WEPeer(button, 'WEMenu');
    try{ x = currentDropDown; }
    catch(e){ window.currentDropDown = null; }
    if(currentDropDown != menu){
    WEHideElement(currentDropDown);
    }
    currentDropDown = menu;
    WEToggleDropDown(currentDropDown);
}

function WECloseMenu()
{
    try{ x = closeCurrentDropDown; }
    catch(e){ window.currentDropDown = null; }
    WEHideElement(currentDropDown);
}

function WESelectText(element, start, end)
{
    var element = WEGetElement(element);
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

function WEStripLeadingZeros(someStr)
{
   var someStr2 = String(someStr);
   if(someStr2 == '0')
       return someStr2;
   return someStr2.replace(/^[0]+/, '');
}

function WEOpenPopup(popupName, popupURL, popupParent)
{
    var popupName = WEReplaceAll(popupName, ' ', '');
    return window.open(popupURL, popupName, "width=800,height=600,toolbar=no,focus=true,scrollbars=yes,resizable=yes");
}

function WEOpenPopupFrame(popupName, popupURL, popupParent)
{
    if(IS_IOS)
    {
        return WEOpenPopup(popupName, popupURL, popupParent);
    }

    if(parent != window)
    {
        if(!popupParent)
        {
            return parent.WEOpenPopup(myPopupName + '-' + popupName, popupURL, myPopupName);
        }
        else
        {
            return parent.WEOpenPopup(popupName, popupURL, popupParent);
        }
    }
    else if(WEInList(openPopups, popupName))
    {
        WESelectPopup(popupName);
        return false;
    }

    if(openPopups.length > 0 && !WEHasClass('popupBackground', 'Enabled'))
    {
        WETogglePopupDisplay()
    }
    else
    {
        WEAddClass(WEGetElement('popupBackground'), 'Enabled')
        WEAddClass(WEGetElement('popupToggle'), 'Enabled')
        if(IS_IOS)
        {
            WEGetElement('body').style.maxHeight = (window.innerHeight - 300) + "px";
            WEGetElement('body').style.width = window.innerHeight + "px";
            WEGetElement('body').style.overflow = "hidden";
        }
    }
    openPopups.push(popupName)

    var newPopupLink = document.createElement('a');
    newPopupLink.setAttribute('id', popupName + "PopUpTab");
    newPopupLink.setAttribute('href', "#LINK");
    newPopupLink.onclick = function(){WESelectPopup(popupName); return false;};
    newPopupLink.appendChild(document.createTextNode(popupName))
    WEGetElement('popupTabs').appendChild(newPopupLink)
    var newPopupContent = document.createElement('iframe');
    if(popupURL.indexOf("?") == -1)
    {
        popupURL = popupURL + "?myPopupName=" + popupName;
    }
    else
    {
        popupURL = popupURL + "&myPopupName=" + popupName
    }
    if(popupParent)
    {
        popupURL = popupURL + "&myPopupParent=" + popupParent
    }
    newPopupContent.setAttribute('id', popupName + "PopUpContents");
    newPopupContent.setAttribute('src', popupURL);
    if(IS_IOS)
    {
        newPopupContent.setAttribute('scrolling', "no");
        if(!WEInList(['MappingFlightPlan', 'MappingRoute'], popupName))
        {
            newPopupContent.style.minHeight = "8000px";
        }
    }
    WEGetElement('popupContents').appendChild(newPopupContent);

    WESelectPopup(popupName);

    return false;
}

function WEWindowOpenProxy(url, popupName, parameters)
{
    if(!popupName || popupName == "_blank")
    {
        var urlSplit = url.split("?")[0].split("/");
        popupName = urlSplit[urlSplit.length -1];
        popupName = popupName.split("?")[0];
        popupName = popupName.split("#")[0];
        popupName += Math.floor((Math.random()*100000)+1);
    }
    var popupName = WEReplaceAll(popupName, ' ', '');
    window.open(url, popupName, parameters);
}

function WEClosePopup(popupName)
{
    if(parent != window)
    {
        return parent.WEClosePopup(popupName);
    }

    if(!popupName){
        var popupName = selectedPopup;
    }
    WERemoveElement(popupName + "PopUpTab");
    WERemoveElement(popupName + "PopUpContents");
    openPopups = WERemoveFromArray(openPopups, popupName);
    delete openPopupFrames[popupName];
    if(openPopups.length <= 0)
    {
        WERemoveClass(WEGetElement('popupBackground'), 'Enabled');
        WERemoveClass(WEGetElement('popupToggle'), 'Enabled');
        if(IS_IOS)
        {
            WEGetElement('body').style.maxHeight = null;
            WEGetElement('body').style.width = null;
            WEGetElement('body').style.overflow = null;
        }
        selectedPopup = null;
    }
    else if(popupName == selectedPopup)
    {
        selectedPopup = null;
        WESelectPopup(openPopups[openPopups.length - 1]);
    }
}

var selectedPopup = null;
function WESelectPopup(popupName)
{
    if(parent != window)
    {
        return parent.WESelectPopup(popupName);
    }
    if(openPopups.length > 0 && !WEHasClass('popupBackground', 'Enabled'))
    {
        WETogglePopupDisplay()
    }
    if(selectedPopup)
    {
        WERemoveClass(selectedPopup + "PopUpTab", "Selected");
        WERemoveClass(selectedPopup + "PopUpContents", "Selected");
    }

    if(IS_IOS)
    {
        WEGetElement("popupContents").scrollTo(0, 0);
    }

    WEAddClass(popupName + "PopUpTab", "Selected");
    WEAddClass(popupName + "PopUpContents", "Selected");
    selectedPopup = popupName;
}

function WETogglePopupDisplay()
{
    var popupDisplay = WEGetElement('popupBackground');
    var popupToggle = WEGetElement('popupToggle');
    if(WEHasClass(popupDisplay, 'Enabled'))
    {
        WERemoveClass(popupDisplay, 'Enabled');
        popupToggle.innerHTML = "You have open tasks / windows; click here to view.";
    }
    else
    {
        WEAddClass(popupDisplay, 'Enabled');
        popupToggle.innerHTML = "Click here to return to the main window.";
    }
}

function WEScrolledToBottom(scroller)
{
    var scroller = WEGetElement(scroller);
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

function WEPopupUnload()
{
    if( openPopups.length > 0 )
    {
        return "You have unresolved pop-up notifications.";
    }
}

function WEAddToForm(popupName, popupParent)
{
    for(var currentFormIndex = 0; currentFormIndex < document.forms.length; currentFormIndex++)
    {
        var currentForm = document.forms[currentFormIndex];
        var newPopupValue = document.createElement('input');
        newPopupValue.setAttribute('id', "myPopupName");
        newPopupValue.setAttribute('name', "myPopupName");
        newPopupValue.setAttribute('value', popupName);
        newPopupValue.setAttribute('type', "hidden");
        currentForm.appendChild(newPopupValue);

        if(popupParent)
        {
            var newPopupValue = document.createElement('input');
            newPopupValue.setAttribute('id', "myPopupParent");
            newPopupValue.setAttribute('name', "myPopupParent");
            newPopupValue.setAttribute('value', popupParent);
            newPopupValue.setAttribute('type', "hidden");
            currentForm.appendChild(newPopupValue);
        }
    }
}

function WEDetatchPopup(poupName)
{
    if(parent != window)
    {
        return parent.WEDetatchPopup(popupName);
    }

    if(!popupName)
    {
        var popupName = selectedPopup;
    }

    Popup.open({url:openPopupFrames[popupName].location.href, separateWindow:true, width:800, height:600})
    WEClosePopup(popupName);

    return false;
}

function WERegisterPopup(popupName, popupParent)
{
    window.myPopupName = popupName;
    window.myPopupParent = popupParent;
    if(popupParent)
    {
        opener = parent.openPopupFrames[popupParent];
    }
    for(var currentFrameIndex = 0; currentFrameIndex < parent.frames.length; currentFrameIndex++)
    {
        var currentFrame = parent.frames[currentFrameIndex];
        if(currentFrame.frameElement.id == (popupName + "PopUpContents"))
        {
            parent.openPopupFrames[popupName] = currentFrame;
        }
    }
    setTimeout("WEAddToForm('" + popupName + "', '" + popupParent + "');", 1);
}

// Toggle between Adding or Removing a class from an element.
function WEToggleClass(element, classname )
{
	if(WEHasClass(element, classname))
	{
		WERemoveClass(element, classname);
	}
	else
	{
		WEAddClass(element, classname);
	}
}

// Toggle between selecting/unselecting a row on a table.
function WEToggleTableRowSelect(input)
{
	var row = input
	for (var levels = 3; levels > 0; levels -= 1)
	{
		row = row.parentElement
		if (row.parentElement.tagName == "TR")
		{
			WEToggleClass(row.parentElement, 'selected');
			levels = 0;
		}
	}
}

// Attach popup warning to main window
if(parent == window)
{
    var openPopups = [];
    var openPopupFrames = {};

    if(IS_IOS)
    {
        setTimeout("WEHideElement('popupToggle');", 1);
    }
    else
    {
        var oldBeforeUnload = null;
        if(typeof window.onbeforeunload == "function")
        {
            oldBeforeUnload = window.onbeforeunload;
        }
        window.onbeforeunload = function(){
            try{
                unloadResult = WEPopupUnload()
                if(unloadResult)
                {
                    return unloadResult;
                }
                else if(oldBeforeUnload != null)
                {
                    return oldBeforeUnload();
                }
            }
            catch(e)
            {
            }
        }
        var oldUnload = null;
        if(typeof window.unload == "function")
        {
            oldUnload = window.unload;
        }
        window.onunload = function(){
            try{
                if(oldUnload != null)
                {
                    return oldUnload();
                }
            }
            catch(e)
            {
            }
            delete openPopups;
            delete openPopupFrames;
        }
    }
}
else
{
    opener = parent;
    eval("function close(){return WEClosePopup(myPopupName);}");
    if(IS_IOS)
    {
        setTimeout("parent.WEGetElement('popupContents').scrollTo(0, 0);", 1);
        document.startY = 0;
        document.startX = 0;
        setTimeout(function () {
            document.frameBody = document.body;
            document.frameBody.addEventListener('touchstart', function (event) {
                parent.window.scrollTo(0, 1);
                document.startY = event.targetTouches[0].pageY;
                document.startX = event.targetTouches[0].pageX;
            });
            document.frameBody.addEventListener('touchmove', function (event) {
                event.preventDefault();
                var currentPositionY = event.targetTouches[0].pageY;
                var currentPositionX = event.targetTouches[0].pageX;
                var scroller = parent.document.getElementById("popupContents");
                scroller.scrollTop = scroller.scrollTop + (document.startY - currentPositionY);
                scroller.scrollLeft = scroller.scrollLeft + (document.startX - currentPositionX);
            });
            }, 1);
    }
}


function WEGetNotificationPermission()
{

    if (window.webkitNotifications)
    {
        if (window.webkitNotifications.checkPermission() != 0)
        {
            window.webkitNotifications.requestPermission();
        }
    }
}

function WEShowNotification(title, content, icon)
{
    if(!icon)
    {
        icon = "images/info.png";
    }
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

// Make two checkboxes act like radio button. elem is "this" and pair is the other checkbox
function WECheckboxActsLikeRadioButton(elem, pair)
{
    if(!elem.checked)
        return;
    pair.checked = false;
}
