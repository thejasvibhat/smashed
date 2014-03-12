import sys
import os

sys.path.append (os.path.join(os.path.abspath(os.path.dirname(__file__)), '../lib'))
sys.path.append (os.path.join(os.path.abspath(os.path.dirname(__file__)), '../'))
sys.path.append (os.path.join(os.path.abspath(os.path.dirname(__file__)), '.'))

import cgi
import urllib
import webapp2
import urllib2
import logging

from simpleauth import SimpleAuthHandler
from Cheetah.Template import Template
from postfacebook import PostFacebook
from user import User
from secrets import secrets
from handlers import AuthHandler
from skel.skel import Skel
from webapp2_extras import auth, sessions, jinja2, routes

class LandingPage (AuthHandler):

    def get(self):
        redirect_url = self.request.get("redirect_url")
        if redirect_url != "":
            self.session.add_flash (redirect_url,key='redirect_url')         
        path = os.path.join(os.path.dirname(__file__), 'templates/landingpage.tmpl')
        template_values = {'logout_url': '/auth/logout'}
        l_auth = auth.get_auth()

        if l_auth.get_user_by_session():
            user_dict = l_auth.get_user_by_session()
            username = l_auth.store.user_model.get_by_id (user_dict['user_id'])
            template_values.update ({'user_loggedin' : 1,
                                     'username': username})
        else:
            template_values.update ({'user_loggedin' : 0})

        #render template with values inserted
        tmpl = Template( file = path, searchList = (template_values,) )

        #output the template to screen
        self.response.out.write(tmpl)

class SelfProfileHandler(AuthHandler):
    def get(self):
        # self._gatekeeper ("addBar")
        l_skel = Skel()
        l_skel.title = "Smashed.in :: Me"

        template_values = {
            "user" : self.user,
            "session1" : self.auth.get_user_by_session()
            }
        path = os.path.join (os.path.dirname (__file__), 'templates/me-body.tmpl')
        l_skel.addtobody (str((Template.compile(file=path) (searchList=template_values))))

        self.response.out.write(l_skel.gethtml())

    # def _gatekeeper (self, action):
    #     if self.user.hasPermission.addBar is not True:
    #         return
    #     self.abort (500, headers={"X-error" : "This is shit"}, detail="Details", comment="No comments")

class ProfileHandler(AuthHandler):
    def get (self, user):
        #TODO
        l_skel = Skel()
        l_skel.title = "Smashed.in :: MerryMaker"

        template_values = {
            "user" : "fellow drinker",
            "session1" : "session partner"
            }
        path = os.path.join (os.path.dirname (__file__), 'templates/profile-body.tmpl')
        l_skel.addtobody (str((Template.compile(file=path) (searchList=template_values))))

        self.response.out.write(l_skel.gethtml())

# webapp2 config
app_config = {
  'webapp2_extras.sessions': {
    'cookie_name': '_simpleauth_sess',
    'secret_key': secrets.SESSION_KEY
  },
  'webapp2_extras.auth': {
    'user_attributes': [],
    'user_model' : User,
    'token_max_age': 86400 * 365 * 4
  }
}

# Map URLs to handlers
auth_routes = [

  routes.RedirectRoute ('/auth', handler=LandingPage, name="auth", strict_slash=True),
  routes.RedirectRoute ('/merrymaker',
                        handler=SelfProfileHandler, name='selfprofile', strict_slash=True),
  routes.RedirectRoute ('/merrymaker/<user>',
                        handler=ProfileHandler, name='profile', strict_slash=True),

  routes.RedirectRoute ('/auth/logout',
                 handler='handlers.AuthHandler:logout', name='logout', strict_slash=True),
  webapp2.Route ('/auth/post/<provider>',
                 handler=PostFacebook, name='auth_login'),

  webapp2.Route ('/auth/<provider>',
                 handler='handlers.AuthHandler:_simple_auth', name='auth_login'),
  webapp2.Route ('/auth/<provider>/callback',
                 handler='handlers.AuthHandler:_auth_callback', name='auth_callback')
]

def handle_404 (request, response, exception):
    logging.exception (exception)
    response.write ('Oops! I could swear this page was here!')
    response.set_status (404)

def handle_500 (request, response, exception):
    logging.exception (exception)
    response.write ('Server did not see this coming.!')
    response.set_status (500)

application = webapp2.WSGIApplication (auth_routes, config=app_config, debug=True)

application.error_handlers[500] = handle_500
application.error_handlers[404] = handle_404
