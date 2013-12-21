import sys
import os

sys.path.insert (0, os.path.join(os.path.abspath(os.path.dirname(__file__)), '../lib'))
sys.path.insert (0, os.path.join(os.path.abspath(os.path.dirname(__file__)), '../'))

import logging
from secrets import secrets
from skel.skelerr import SkelErr
import webapp2
from webapp2_extras import auth, sessions

from simpleauth import SimpleAuthHandler

class BaseRequestHandler(webapp2.RequestHandler):
  def dispatch(self):
    # Get a session store for this request.
    self.session_store = sessions.get_store(request=self.request)
    
    try:
      # Dispatch the request.
      webapp2.RequestHandler.dispatch(self)
    finally:
      # Save all sessions.
      self.session_store.save_sessions(self.response)
    
  @webapp2.cached_property
  def session(self):
    """Returns a session using the default cookie key"""
    return self.session_store.get_session()
    
  @webapp2.cached_property
  def auth(self):
      return auth.get_auth()
  
  @webapp2.cached_property
  def current_user(self):
    """Returns currently logged in user"""
    user_dict = self.auth.get_user_by_session()
    return self.auth.store.user_model.get_by_id(user_dict['user_id'])
      
  @webapp2.cached_property
  def logged_in(self):
    """Returns true if a user is currently logged in, false otherwise"""
    return self.auth.get_user_by_session() is not None

  def render(self, exception):
    # values = {
    #   'url_for': self.uri_for,
    #   'logged_in': self.logged_in,
    #   'flashes': self.session.get_flashes()
    # }

    # values.update(exception)

    l_skel = SkelErr()
    l_skel.title = "Smashed.in :: Pukeee.. "
    l_skel.logged_in = self.logged_in

    message = "Have not found what you are looking for."
    if isinstance(exception, webapp2.HTTPException):
      self.response.set_status(exception.code)
      if exception.code == 403:
        message = "Page under construction. We developers are too sober to open this yet"
    else:
      self.response.set_status (500)

    l_skel.addtobody (message)    
    self.response.out.write (l_skel.gethtml())

  def head(self, *args):
    """Head is used by Twitter. If not there the tweet button shows 0"""
    pass


class AuthHandler(BaseRequestHandler, SimpleAuthHandler):
  """Authentication handler for OAuth 2.0, 1.0(a) and OpenID."""

  # Enable optional OAuth 2.0 CSRF guard
  OAUTH2_CSRF_STATE = True
  
  USER_ATTRS = {
    'facebook' : {
      'id'     : lambda id: ('avatar_url', 
        'http://graph.facebook.com/{0}/picture?type=large'.format(id)),
      'name'   : 'name',
      'link'   : 'link'
    },
    'google'   : {
      'picture': 'avatar_url',
      'name'   : 'name',
      'profile': 'link'
    },
  }

  @webapp2.cached_property
  def user_id (self):
    return self.current_user.key.id()
  @webapp2.cached_property
  def user_name (self):
    return self.current_user.name
  @webapp2.cached_property
  def isloggedin (self):
    return self.logged_in

  @webapp2.cached_property
  def user (self):
    return self.current_user

  def _on_signin(self, data, auth_info, provider):
    """Callback whenever a new or existing user is logging in.
     data is a user info dictionary.
     auth_info contains access token or oauth token and secret.
    """
    auth_id = '%s:%s' % (provider, data['id'])
    logging.info('Looking for a user with id %s', auth_id)
    
    user = self.auth.store.user_model.get_by_auth_id(auth_id)
    _attrs = self._to_user_model_attrs(data, self.USER_ATTRS[provider])

    if user:
      logging.info('Found existing user to log in')
      # Existing users might've changed their profile data so we update our
      # local model anyway. This might result in quite inefficient usage
      # of the Datastore, but we do this anyway for demo purposes.
      #
      # In a real app you could compare _attrs with user's properties fetched
      # from the datastore and update local user in case something's changed.
      user.populate(**_attrs)
      user.put()
      self.auth.set_session(
        self.auth.store.user_to_dict(user))
      
    else:
      # check whether there's a user currently logged in
      # then, create a new user if nobody's signed in, 
      # otherwise add this auth_id to currently logged in user.

      if self.logged_in:
        logging.info('Updating currently logged in user')
        
        u = self.current_user
        u.populate(**_attrs)
        # The following will also do u.put(). Though, in a real app
        # you might want to check the result, which is
        # (boolean, info) tuple where boolean == True indicates success
        # See webapp2_extras.appengine.auth.models.User for details.
        u.add_auth_id(auth_id)
        
      else:
        logging.info('Creating a brand new user')
        ok, user = self.auth.store.user_model.create_user(auth_id, **_attrs)
        if ok:
          self.auth.set_session(self.auth.store.user_to_dict(user))

    # Remember auth data during redirect, just for this demo. You wouldn't
    # normally do this.
    #self.session.add_flash(data, 'data - from _on_signin(...)')
    #self.session.add_flash(auth_info, 'auth_info - from _on_signin(...)')

    # Go to the profile page
    url = self.session.get_flashes (key='redirect_url')
    if not url:
      self.redirect ("/")
      return
    url = url[0][0]
    url = str(url) if url else "/"
    logging.info ("redirecting to %s" % url)
    self.redirect(url)

  def logout(self):
    self.auth.unset_session()
    #UC: Use the following file is developers start using session/user interchangeably.
    #self.session.clear()
    self.redirect('/')

  def handle_exception(self, exception, debug):
    logging.exception (exception)
    self.render(exception)
    
  def _callback_uri_for(self, provider):
    return self.uri_for('auth_callback', provider=provider, _full=True)
    
  def _get_consumer_info_for(self, provider):
    """Returns a tuple (key, secret) for auth init requests."""
    return secrets.AUTH_CONFIG[provider]
    
  def _to_user_model_attrs(self, data, attrs_map):
    """Get the needed information from the provider dataset."""
    user_attrs = {}
    for k, v in attrs_map.iteritems():
      attr = (v, data.get(k)) if isinstance(v, str) else v(data.get(k))
      user_attrs.setdefault(*attr)

    return user_attrs

  def user_gatekeeper (self):
    logging.info ("logged in %s" % str(self.request.path_url))
    if not self.logged_in:
      self.session.add_flash (self.request.path_url, key='redirect_url')
      self.redirect('/auth/')
      self.abort (302)

