"""
    Social.py

    Contains elements that enable connecting with external social sites.

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
"""

from . import Factory
from .Base import WebElement
from .Buttons import Link
from .Display import Image

Factory = Factory.Factory("Social")


class Social(WebElement):
    __slots__ = ('account')
    properties = WebElement.properties.copy()
    properties['account'] = {'action':'classAttribute'}

    def _create(self, name=None, id=None, parent=None, html=""):
        WebElement._create(self, None, None, parent)

        self.account = ""

class TwitterBadge(Social):
    """
        Displays a clickable twitter badge.
    """

    def toHTML(self, formatted=False, *args, **kwargs):
        """
            Returns the twitter badge as defined by the api directly
        """
        return ("""<a href="https://twitter.com/%(account)s" class="twitter-follow-button" """ + \
                """data-show-count="false">Follow @%(account)s</a><script>!function(d,s,id){""" + \
                """var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement""" + \
                """(s);js.id=id;js.src="//platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(""" + \
                """js,fjs);}}(document,"script","twitter-wjs");</script>""") % {'account':self.account}

Factory.addProduct(TwitterBadge)


class GooglePlusBadge(Social):
    """
        Displays a clickable google plus badge.
    """
    __slots__ = ('link', )

    def _create(self, name=None, id=None, parent=None, html=""):
        Social._create(self, None, None, parent)

        self.link = self.addChildElement(Link())
        self.link.attributes['rel'] = "publisher"
        self.link.addClass("WGooglePlusBadge")
        self.link += Image(src="https://ssl.gstatic.com/images/icons/gplus-32.png", alt="Google+")

    def _render(self):
        self.link.setDestination("https://plus.google.com/%s?prsrc=3" % self.account)

Factory.addProduct(GooglePlusBadge)


class FacebookLike(Social):
    """
        Adds a facebook like link to your site
    """
    def toHTML(self, formatted=False, *args, **kwargs):
        return ("""<div class="fb-like" data-href="https://www.facebook.com/%s" data-send="true""" + \
                """data-layout="button_count" data-width="450" data-show-faces="true"></div>""") % self.account

Factory.addProduct(FacebookLike)


class FacebookAPI(WebElement):
    """
        Adds facebook api support to your site - only add once.
    """
    def toHTML(self, formatted=False, *args, **kwargs):
        """
            Returns the api support code directly
        """
        return ("""<div id="fb-root"></div>
                    <script>(function(d, s, id) {
                    var js, fjs = d.getElementsByTagName(s)[0];
                    if (d.getElementById(id)) return;
                    js = d.createElement(s); js.id = id;
                    js.src = "//connect.facebook.net/en_US/all.js#xfbml=1&appId=128897293878199";
                    fjs.parentNode.insertBefore(js, fjs);
                    }(document, 'script', 'facebook-jssdk'));</script>""")

Factory.addProduct(FacebookAPI)
