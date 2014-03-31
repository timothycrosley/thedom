'''
    Compile.py
    
    Provides utilities for taking Node Template files and turning them into optimized python code.

    Classes and methods that aid in creating python dictionaries from XML or SHPAML templates

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

from .All import Factory
from .MultiplePythonSupport import *
from .Types import StyleDict

INDENT = "    "
SCRIPT_TEMPLATE = """# WARNING: DON'T EDIT AUTO-GENERATED

from thedom.Base import Node, TextNode
from thedom.Display import CacheElement, StraightHTML

elementsExpanded = False
%(cacheElements)s
%(staticElements)s


class Template(Node):
    __slots__ = %(accessors)s


def build(factory):
    template = Template()
    
    global elementsExpanded
    if not elementsExpanded:
        products = factory.products
        %(defineElements)s
        elementsExpanded = True
    %(buildTemplate)s
    
    return template"""


class CompiledTemplate(object):
    """
        Represents a template that has been compiled and exec'd in the current runtime, produces a new Node
        representation of the template every time you call you call 'build()' behaving in a similar fashion as
        templates that have been compiled and saved into python modules.
    """
    __slots__ = ('execNamespace', 'factory')
    def __init__(self, execNamespace, factory):
        self.execNamespace = execNamespace
        self.factory = factory
        
    def build(self, factory=None):
        """
            Returns a Node representation of the template using the specified factory.
        """
        factory = factory or self.factory
        return self.execNamespace['build'](factory)
        
    @classmethod
    def create(self, template, factory=Factory):
        """
            Compiles a template in the current python runtime into optimized python bytecode using compile and exec
            returns a CompiledTemplate instance.
        """
        code = compile(toPython(template, Factory), '<string>', 'exec')
        nameSpace = {}
        exec(code, nameSpace)
        return CompiledTemplate(nameSpace, Factory)

def toPython(template, factory=Factory):
    """
        Takes a UITemplate.Template() and a factory, and returns python code that will generate the expected
        Node structure.
    """
    return __createPythonFromTemplate(template, factory)

def __createPythonFromTemplate(template, factory=None, parentNode=None, instance=0, elementsUsed=None,
                               accessorsUsed=None, cacheElements=None, staticElements=None, indent=1):
    python = ""
    if elementsUsed is None:
        elementsUsed = set()
    if accessorsUsed is None:
        accessorsUsed = set()
    if cacheElements is None:
        cacheElements = set()
    if staticElements is None:
        staticElements = set()
    if not parentNode:
        parentNode = "template"

    indented = INDENT * indent
    newNode = "element" + str(instance)
    instance += 1
    if type(template) in (str, unicode):
        if not template:
            instance -= 1
            return ("", instance)
        python += "\n%s%s = %s.add(" % (indented, newNode, parentNode)
        python += 'TextNode("' + template + '"), ensureUnique=False)'
        return (python, instance)

    (accessor, id, name, create, properties, children) = (template.accessor, template.id, template.name,
                                                          template.create, template.properties, template.childElements)
    elementsUsed.add(create)
    element = factory.products[create]
    create = create.replace("-", "_")
    if create in ("and", "or", "with", "if", "del", "template"):
        create = "_" + create
        
    accessor = accessor or id
    if accessor:
        accessor = accessor.replace("-", "_")

    isCached = False
    if create.endswith("cacheelement"):
        cacheElements.add(newNode)
        isCached = True
        python += "\n%s%s = globals()['%s']" % (indented, newNode, newNode)
        python += "\n%sif not %s.rendered():" % (indented, newNode)
        python += "\n%s%s = CacheElement()" % (indented + INDENT, newNode)
        python += "\n%sglobals()['%s'] = %s" % (indented + INDENT, newNode, newNode)
    elif create in ("static", "display-static") and parentNode != "template":
        html = CompiledTemplate.create(template, factory).build(factory).toHTML()
        staticElements.add('%s = StraightHTML(html="""%s""")' % (newNode, html))
        python += "\n%s%s.add(%s, ensureUnique=False)" % (indented, parentNode, newNode)
        return (python, instance)
    else:
        python += '\n%s%s = %s(id=%s, name=%s, parent=%s)' % (indented, newNode, create.lower(), repr(id),
                                                              repr(name), parentNode)
    for name, value in properties:
        if value is not None and name in element.properties:
            propertyDict = element.properties[name]
            propertyActions = propertyDict['action'].split('.')
            propertyAction = propertyActions.pop(-1)
            if propertyActions:
                propertyActions = "." + ".".join(propertyActions)
            else:
                propertyActions = ""
            propertyName = propertyDict.get('name', name)
            
            if propertyAction == "classAttribute":
                python += "\n%s%s%s.%s = %s" % (indented, newNode, propertyActions, propertyName, repr(value))
            elif propertyAction == "attribute":
                python += "\n%s%s%s.attributes[%s] = %s" % (indented, newNode, propertyActions, repr(propertyName),
                                                            repr(value))
            elif propertyAction == "javascriptEvent":
                python += "\n%s%s%s.addJavascriptEvent(%s, %s)" % (indented, newNode, propertyActions,
                                                                   repr(propertyName), repr(value))
            elif propertyAction == "call":
                if value:
                    python += "\n%s%s%s.%s()" % (indented, newNode, propertyActions, propertyName)
            elif propertyAction == "send":
                python += "\n%s%s%s.%s(%s, %s)" % (indented, newNode, propertyActions,
                                                                   propertyName, repr(name), repr(value))
            elif propertyAction == "addClassesFromString":
                python += "\n%s%s%s.addClasses(%s)" % (indented, newNode, propertyActions,
                                                       repr(tuple(value.split(" "))))
            elif propertyAction == "setStyleFromString":
                python += "\n%s%s%s.style.update(%s)" % (indented, newNode, propertyActions,
                                                         repr(StyleDict.fromString(value)))
            else:
                python += "\n%s%s%s.%s(%s)" % (indented, newNode, propertyActions, propertyAction, repr(value))
            
    if accessor:
        accessorsUsed.add(accessor)
        python += "\n%stemplate.%s = %s" % (indented, accessor, newNode)

    if children:
        if isCached:
            childAccessors = set()
            childIndent = indent + 1
        else:
            childAccessors = accessorsUsed
            childIndent = indent
        for node in children:
            (childPython, instance) = __createPythonFromTemplate(node, factory, newNode, instance, elementsUsed,
                                                            childAccessors, cacheElements, staticElements, childIndent)
            python += childPython
        if isCached:
            if childAccessors:
                accessorsUsed.update(childAccessors)
                python += "\n%selse:" % indented
                for accessor in childAccessors:
                    python += "\n%stemplate.%s = %s" % (indented + INDENT, accessor, newNode)
                
            
    python += "\n%s%s.add(%s, ensureUnique=False)" % (indented, parentNode, newNode)
    if parentNode == "template":
        defineElements = ""
        for elementName in elementsUsed:
            variableName = elementName.replace("-", "_")
            if variableName in ("and", "or", "with", "if", "del", "template"):
                variableName = "_" + variableName
            defineElements += "globals()['%s'] = products['%s']\n%s" % (variableName, elementName, INDENT * 2)
            
        cacheDefinitions = ""
        for elementName in cacheElements:
            cacheDefinitions += "%s = CacheElement()\n" % elementName
        
        return SCRIPT_TEMPLATE % {'accessors':tuple(accessorsUsed), 'buildTemplate':python,
                                  'defineElements':defineElements, 'cacheElements':cacheDefinitions,
                                  'staticElements':"\n".join(staticElements)}
        
        
    return (python, instance)
