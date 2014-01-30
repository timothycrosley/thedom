![webelements](https://raw.github.com/timothycrosley/webelements/develop/logo.png)
=====

[![PyPI version](https://badge.fury.io/py/webelements.png)](http://badge.fury.io/py/webelements)
[![PyPi downloads](https://pypip.in/d/webelements/badge.png)](https://crate.io/packages/webelements/)
[![Build Status](https://travis-ci.org/timothycrosley/webelements.png?branch=master)](https://travis-ci.org/timothycrosley/webelements)
[![License](https://pypip.in/license/webelements/badge.png)](https://pypi.python.org/pypi/webelements/)
[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/timothycrosley/webelements/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

WebElements is a collection of python objects that enable developers to generate and interact with web apps server side.
It encourages object oriented website development, and code reuse by seperating each DOM element into its own object,
and then allowing inheritance and child elements to come together to form new elements not defined in the standard DOM.

write this:

    from WebElements import Layout, Document, Buttons

    page = Document.Document()
    layout = page.addChildElement(Layout.Center()).addChildElement(Layout.Horizontal())
    layout += Buttons.Button(text="Use WebElements.", **{'class':'MainAction'})
    layout += Buttons.Button(text="Enjoy writing less code.", **{'class':'DeleteAction'})
    layout += Buttons.Button(text="100% Python.")

    print page.toHTML(formatted=True)

get this:

    <!DOCTYPE html>
    <html>
        <head>
        <title>
        </title>
        <meta content="text/html; charset=UTF-8" http-equiv="Content-Type">
        </meta>
        </head>
        <body>
            <div class="WCenter">
                <div class="WOuter">
                    <div class="WInner">
                        <div class="WClear">
                            <input class="WBlock WLeft MainAction" type="button" value="Use WebElements." />
                            <input class="WBlock WLeft DeleteAction" type="button" value="Enjoy writing less code." />
                            <input class="WBlock WLeft" type="button" value="100% Python." />
                        </div>
                    </div>
                </div>
            </div>
        </body>
    </html>

Installing WebElements
===================

Installing WebElements is as simple as:

    pip install webelements

or if you prefer

    easy_install webelements

--------------------------------------------

Thanks and I hope you find WebElements useful!

~Timothy Crosley
