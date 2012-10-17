#!/usr/bin/python
'''
   Name:
       All.py

   Description:
        A Factory that contains all the base WebElements, additionally can be used to import all WebElements with
        a single import (for example: import WebElements.All as WebElements; layout = WebElements.Layout.Vertical())
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
