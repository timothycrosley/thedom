"""
    Defines an AppEngine compatible version of DynamicForm
"""

import webapp2
from webapp2_extras import sessions
from . import HTTP, PageControls
from .DynamicForm import DynamicForm


def adapt(dynamicForm):
    """
        Takes a dynamicForm class and returns an optimized app engine request handler
    """
    class Adaptor(webapp2.RequestHandler):
        """
            Overrides handler methods of the DynamicForm class to enable it to run seamlessly on AppEngine
        """
        form = dynamicForm()

        def get(self):
            response = self.form.handleRequest(HTTP.Request.fromAppEngineRequest(self.request, "GET", self.session))
            return response.toAppEngineResponse(self.response)

        def post(self):
            response = self.form.handleRequest(HTTP.Request.fromAppEngineRequest(self.request, "POST", self.session))
            return response.toAppEngineResponse(self.response)

        def put(self):
            response = self.form.handleRequest(HTTP.Request.fromAppEngineRequest(self.request, "PUT", self.session))
            return response.toAppEngineResponse(self.response)

        def head(self):
            response = self.form.handleRequest(HTTP.Request.fromAppEngineRequest(self.request, "HEAD", self.session))
            return response.toAppEngineResponse(self.response)

        def options(self):
            response = self.form.handleRequest(HTTP.Request.fromAppEngineRequest(self.request, "OPTIONS", self.session))
            return response.toAppEngineResponse(self.response)

        def delete(self):
            response = self.form.handleRequest(HTTP.Request.fromAppEngineRequest(self.request, "DELETE", self.session))
            return response.toAppEngineResponse(self.response)

        def trace(self):
            response = self.form.handleRequest(HTTP.Request.fromAppEngineRequest(self.request, "TRACE", self.session))
            return response.toAppEngineResponse(self.response)
        
        def dispatch(self):
            """
            This snippet of code is taken from the webapp2 framework documentation.
            See more at
            http://webapp-improved.appspot.com/api/webapp2_extras/sessions.html

            """
            self.session_store = sessions.get_store(request=self.request)
            try:
                webapp2.RequestHandler.dispatch(self)
            finally:
                self.session_store.save_sessions(self.response)

        @webapp2.cached_property
        def session(self):
            """
            This snippet of code is taken from the webapp2 framework documentation.
            See more at
            http://webapp-improved.appspot.com/api/webapp2_extras/sessions.html

            """
            return self.session_store.get_session()

    return Adaptor
