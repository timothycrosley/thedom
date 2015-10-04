![thedom](https://raw.github.com/timothycrosley/thedom/develop/logo.png)
=====

[![PyPI version](https://badge.fury.io/py/thedom.png)](http://badge.fury.io/py/thedom)
[![PyPi downloads](https://pypip.in/d/thedom/badge.png)](https://crate.io/packages/thedom/)
[![Build Status](https://travis-ci.org/timothycrosley/thedom.png?branch=master)](https://travis-ci.org/timothycrosley/thedom)
[![License](https://pypip.in/license/thedom/badge.png)](https://pypi.python.org/pypi/thedom/)
[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/timothycrosley/thedom/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

thedom is a collection of python objects that enable developers to generate and interact with web apps server side.
It encourages object oriented website development, and code reuse by seperating each DOM element into its own object,
and then allowing inheritance and child elements to come together to form new elements not defined in the standard DOM.

write this:

    from thedom import layout, document, buttons

    page = document.Document()
    layout = page.addChildElement(layout.Center()).addChildElement(layout.Horizontal())
    layout += buttons.Button(text="Use thedom.", **{'class':'MainAction'})
    layout += buttons.Button(text="Enjoy writing less code.", **{'class':'DeleteAction'})
    layout += buttons.Button(text="100% Python.")

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
                            <input class="WBlock WLeft MainAction" type="button" value="Use thedom." />
                            <input class="WBlock WLeft DeleteAction" type="button" value="Enjoy writing less code." />
                            <input class="WBlock WLeft" type="button" value="100% Python." />
                        </div>
                    </div>
                </div>
            </div>
        </body>
    </html>

Installing thedom
===================

Installing thedom is as simple as:

    pip install thedom

or if you prefer

    easy_install thedom

--------------------------------------------

Thanks and I hope you find thedom useful!

~Timothy Crosley
