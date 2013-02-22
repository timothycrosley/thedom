'''
    All.py

    A Factory that contains all the base WebElements, additionally can be used to import all WebElements with
    a single import (for example: import WebElements.All as WebElements; layout = WebElements.Layout.Vertical())

    Copyright (C) 2013  Timothy Edmund Crosley

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty
     ,  of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''

from . import (Base,
               Buttons,
               Charts,
               CodeDocumentation,
               Containers,
               DataViews,
               Display,
               Document,
               DOM,
               Factory,
               Fields,
               HiddenInputs,
               HTML5,
               Inputs,
               Layout,
               Navigation,
               Printing,
               Resources,
               UITemplate,
               Validators,
               Social)

FactoryClasses = Factory
Factory = Factory.Composite((Validators.Factory, DOM.Factory, Buttons.Factory, DataViews.Factory,
                             Display.Factory, Fields.Factory, HiddenInputs.Factory, Inputs.Factory,
                             Layout.Factory, Navigation.Factory, Resources.Factory, Containers.Factory,
                             Charts.Factory, Printing.Factory, Document.Factory, CodeDocumentation.Factory,
                             HTML5.Factory, Social.Factory))
