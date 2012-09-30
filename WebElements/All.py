#!/usr/bin/python
'''
   Name:
       WebElements.py

   Description:
       WebElements enable highly flexible "widgets" or entire Web Applications
       to be built from dictionaries, xml, or WebElement objects dynamically modified
       and then converted to HTML on the fly
'''

import Ajax
import Base
import Buttons
import Charts
import Containers
import DataViews
import Display
import Document
import DOM
import Factory
import Fields
import HiddenInputs
import Inputs
import Layout
import Navigation
import Printing
import Resources
import HTML5
import UITemplate
import CodeDocumentation

FactoryClasses = Factory
Factory = Factory.Composite((DOM.Factory, Buttons.Factory, Ajax.Factory, DataViews.Factory,
                             Display.Factory, Fields.Factory, HiddenInputs.Factory, Inputs.Factory,
                             Layout.Factory, Navigation.Factory, Resources.Factory, Containers.Factory,
                             Charts.Factory, Printing.Factory, Document.Factory, CodeDocumentation.Factory,
                             HTML5.Factory))
