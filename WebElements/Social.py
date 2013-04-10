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

import hashlib
import urllib

from . import Factory
from .Base import WebElement
from .Buttons import Link
from .Display import Image

Factory = Factory.Factory("Social")


class Social(WebElement):
    __slots__ = ('account')
    properties = WebElement.properties.copy()
    properties['account'] = {'action':'classAttribute'}

    def _create(self, name=None, id=None, parent=None, html="", *kargs, **kwargs):
        WebElement._create(self, None, None, parent, *kargs, **kwargs)

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

    def _create(self, name=None, id=None, parent=None, html="", *kargs, **kwargs):
        Social._create(self, None, None, parent, *kargs, **kwargs)

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
        return ("""<div class="fb-like" data-href="https://www.facebook.com/%s" data-send="false""" + \
                """data-layout="button_count" data-width="300" data-show-faces="false"></div>""") % self.account

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


class Gravatar(Image):
    """
        A Gravatar user image based on an email id
    """
    __slots__ = ('email', '_size', '_default', '_rating')
    properties = Image.properties.copy()
    properties['email'] = {'action':'classAttribute'}
    properties['size'] = {'action':'setSize', 'type':'int'}
    properties['rating'] = {'action':'setRating'}
    properties['default'] = {'action':'setDefault'}

    def _create(self, name=None, id=None, parent=None, html="", *kargs, **kwargs):
        Image._create(self, None, None, parent, *kargs, **kwargs)
        self.email = ""
        self._size = 80
        self._default = "mm"
        self._rating = "g"

    def _render(self):
        self.attributes['src'] = "http://www.gravatar.com/avatar/%s?s=%s&r=%s&d=%s" % \
                                  (hashlib.md5(self.email.encode('utf-8')).hexdigest(), self.size(),
                                   self.rating(), self.default())
        self.style['width'] = "%spx" % self.size()
        self.style['height'] = "%spx" % self.size()

    def profileURL(self):
        """
            Returns the associated profile URL that can be used to modify the provided image
        """
        return "http://www.gravatar.com/%s" % hashlib.md5(self.email.encode('utf-8')).hexdigest()

    def setSize(self, size):
        """
            Set the width of the google chart in pixels (maximum allowed by google is 1000 pixels)
        """
        size = int(size)
        if size > 2048 or size < 1:
            raise ValueError("Gravatar only supports requesting image sizes 1 - 2048")
        self._size = size

    def size(self):
        """
            Returns the size of this gravatar
        """
        return self._size

    def setRating(self, rating):
        """
            Sets the maximum rating of the returned image (g, pg, r, or x)
        """
        rating = rating.lower()
        if rating not in ('g', 'pg', 'r', 'x'):
            raise ValueError("Gravatar only supports the ratings g, pg, r, and x")

        self._rating = rating

    def rating(self):
        """
            Returns the maximum rating allowed for this image
        """
        return self._rating

    def setDefault(self, default):
        """
            Sets the default image in the case the provided email does not have a gravatar
            can be a direct url or one of the included defaults:
                404, mm, identicon, monsterid, wavatar, retro, and blank
        """
        self._default = urllib.encode(default)

    def default(self):
        """
            Returns the image set to load if none is available for the specified email address
        """
        return self._default

Factory.addProduct(Gravatar)

