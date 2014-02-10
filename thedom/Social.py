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

from . import ClientSide, Factory, Layout
from .Base import TextNode, Node
from .Buttons import Link
from .Display import Image

Factory = Factory.Factory("Social")


class Social(Node):
    __slots__ = ('account')
    properties = Node.properties.copy()
    properties['account'] = {'action':'classAttribute'}

    def _create(self, name=None, id=None, parent=None, html="", *kargs, **kwargs):
        Node._create(self, None, None, parent, *kargs, **kwargs)

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


class TwitterAPI(Node):
    __slots__ = ()
    def _create(self, name=None, id=None, parent=None, html="", *kargs, **kwargs):
        Node._create(self, name, id, parent, *kargs, **kwargs)
        self.addScript('window.twttr = (function (d,s,id) {'
                       'var t, js, fjs = d.getElementsByTagName(s)[0];'
                       'if (d.getElementById(id)) return; js=d.createElement(s); js.id=id;'
                       'js.src="https://platform.twitter.com/widgets.js"; fjs.parentNode.insertBefore(js, fjs);'
                       'return window.twttr || (t = { _e: [], ready: function(f){ t._e.push(f) } });'
                       '}(document, "script", "twitter-wjs"));')

Factory.addProduct(TwitterAPI)


class Tweet(Link):
    __slots__ = ()
    properties = Link.properties.copy()
    properties['hideCount'] = {'action':'hideCount', 'type':'bool', 'info':"Don't show the number of re-tweets"}
    properties['largeButton'] = {'action':'useLargeButton', 'type':'bool', 'info':'User larger tweet button size'}
    properties['url'] = {'action':'attribute', 'name':'data-url', 'info':'Set the url the tweet will link to'}
    properties['hashtag'] = {'action':'attribute', 'name':'data-hashtags', 'info':'Associated a hashtag to the tweet'}
    properties['via'] = {'action':'attribute', 'name':'data-via', 'info':'Associated with another twitter account'}
    properties['message'] = {'action':'attribute', 'name':'data-text', 'info':'The tweet message text'}
    
    def _create(self, name=None, id=None, parent=None, *kargs, **kwargs):
        Link._create(self, name, id, parent, *kargs, **kwargs)
        self.setText("Tweet")
        self.addClass("twitter-share-button")
        self.setDestination("https://twitter.com/share")
    
    def hideCount(self, hide=True):
        if hide:
            self.attributes['data-count'] = 'none'
        else:
            self.attributes.pop('data-count', None)

    def useLargeButton(self, use=True):
        if use:
            self.attributes['data-size'] = 'large'
        else:
            self.attributes.pop('data-size', None)

    def toHTML(self, formatted=False, *args, **kwargs):
        """
            Adds the twitter script to the tweet button
        """ 
        html = Link.toHTML(self, formatted, *args, **kwargs)
        return html
    
Factory.addProduct(Tweet)


class GooglePlusAPI(Node):
    __slots__ = ()
    def _create(self, name=None, id=None, parent=None, html="", *kargs, **kwargs):
        Node._create(self, name, id, parent, *kargs, **kwargs)
        self.addScript("window.___gcfg = {lang:'en-US','parsetags':'explicit'};"
                       "(function() {var po = document.createElement('script');"
                       "po.type = 'text/javascript'; po.async = true;"
                       "po.src = 'https://apis.google.com/js/plusone.js';"
                       "var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);"
                       "})();")

Factory.addProduct(GooglePlusAPI)


class GooglePlusShare(Layout.Box):
    __slots__ = ()
    properties = Layout.Box.properties.copy()
    properties['size'] = {'action':'attribute', 'name':'data-height', 'type':'int',
                          'info':"The Size of the of the button, 2 is large"}
    properties['url'] = {'action':'attribute', 'name':'data-href', 'info':"The url the google plus button points to"}
    def _create(self, name=None, id=None, parent=None, html="", *kargs, **kwargs):
        Node._create(self, name, id, parent, *kargs, **kwargs)
        self.addClass("g-plus")
        self.attributes['data-action'] = "share"
        self.attributes['data-annotation'] = "none"

Factory.addProduct(GooglePlusShare)


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


class FacebookAPI(Layout.Box):
    """
        Adds facebook api support to your site and optionally calls the init method on it - only add once.
    """
    __slots__ = ('loginURL', 'logoutURL', 'appId', 'init')
    properties = Node.properties.copy()
    properties['appId'] = {'action':'classAttribute'}
    properties['init'] = {'action':'classAttribute', 'type':'bool'}
    properties['loginURL'] = {'action':'classAttribute'}
    properties['logoutURL'] = {'action':'classAttribute'}
    
    class ClientSide(Layout.Box.ClientSide):
        def feed(self, name, caption, description, link, picture=None, redirect=None, callback=None):
            """
                Posts defined data to the users news feed.
            """
            arguments = {'method':'feed', 'name':name, 'caption':caption, 'link':link}
            if picture:
                arguments['picture'] = picture
            if redirect:
                arguments['redirect_url'] = redirect
            if callback:
                return ClientSide.call("FB.ui", arguments, callback)
            if description:
                arguments['description'] = description
            
            return ClientSide.call("FB.ui", arguments)
    
    def _create(self, id=None, name=None, parent=None, *kargs, **kwargs):
        Layout.Box._create(self, "fb-root", name, parent, *kargs, **kwargs)
        self.appId = ""
        self.init = False
        self.loginURL = None
        self.logoutURL = None

    def _render(self):
        """
            Returns the api support code directly
        """
        if self.init:
            extra = ""
            if self.loginURL:
                extra += "FB.Event.subscribe('auth.login', function(response){window.location = '%s'});" % \
                         self.loginURL
            if self.logoutURL:
                extra += "FB.Event.subscribe('auth.logout', function(response){window.location = '%s'});" % \
                         self.logoutURL
            self.addScript("""window.fbAsyncInit = function(){FB.init
                                            ({appId: '%s', status: true, cookie: true, xfbml: true});
                                            %s
                                            }""" % (self.appId, extra))
        self.addScript("""(function(d, s, id){
                            var js, fjs = d.getElementsByTagName(s)[0];
                            if (d.getElementById(id)) {return;}
                            js = d.createElement(s); js.id = id;
                            js.src = "//connect.facebook.net/en_US/all.js";
                            fjs.parentNode.insertBefore(js, fjs);
                        }(document, 'script', 'facebook-jssdk'));""")

Factory.addProduct(FacebookAPI)


class FacebookLogin(Node):
    """
        Adds a facebook login button to the page
    """    
    __slots__ = ('text', )
    tagName = "fb:login-button"
    properties = Node.properties.copy()
    properties['show-faces'] = {'action':'attribute', 'type':'bool',
                                'info':'Specifies whether to show faces underneath the Login button.'}
    properties['width'] = {'action':'attribute', 'type':'int',
                           'info':'The width of the plugin in pixels. Default width: 200px.'}
    properties['size'] = {'action':'attribute',
                          'info':'Different sized buttons: small, medium, large, xlarge (default: medium).'}
    properties['max-rows'] = {'action':'attribute', 'type':'int',
                              'info':'The maximum number of rows of profile pictures to display. Default value: 1.'}
    properties['scope'] = {'action':'attribute', 'info':'a comma separated list of extended permissions to request.'}
    properties['registration-url '] = {'action':'attribute',
                                       'info':'URL to redirect to on initial registration.'}
    properties['text'] = {'action':'classAttribute', 'info':'Set a custom label for the facebook connect button.'}
    
    def _create(self, id=None, name=None, parent=None, *kargs, **kwargs):
        Node._create(self, id, name, parent, *kargs, **kwargs)
        self.text = None
    
    def _render(self):
        if self.text:
            if not self.childElements:
                self += TextNode()
                
            self.childElements[0].setText(self.text)
        elif self.childElements:
            self.childElements[0].setText("")
            
    class ClientSide(Node.ClientSide):
        """
            Defines the client-side behavior of the facebook api.
        """
        def logout(self):
            return ClientSide.call("FB.logout")
        
Factory.addProduct(FacebookLogin)


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
