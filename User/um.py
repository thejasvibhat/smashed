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

from secrets import secrets
from webapp2_extras import auth, sessions, jinja2

class LandingPage (webapp2.RequestHandler):

    def get(self):

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


# webapp2 config
app_config = {
  'webapp2_extras.sessions': {
    'cookie_name': '_simpleauth_sess',
    'secret_key': secrets.SESSION_KEY
  },
  'webapp2_extras.auth': {
    'user_attributes': []
  }
}

# Map URLs to handlers
routes = [

  webapp2.Route ('/auth/', handler=LandingPage),

  webapp2.Route ('/auth/profile',
                 handler='handlers.ProfileHandler', name='profile'),
  webapp2.Route ('/auth/logout',
                 handler='handlers.AuthHandler:logout', name='logout'),
  webapp2.Route ('/auth/<provider>',
                 handler='handlers.AuthHandler:_simple_auth', name='auth_login'),
  webapp2.Route ('/auth/<provider>/callback',
                 handler='handlers.AuthHandler:_auth_callback', name='auth_callback')
]

application = webapp2.WSGIApplication (routes, config=app_config, debug=True)
