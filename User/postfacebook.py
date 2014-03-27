import webapp2
from User.handlers import AuthHandler
from google.appengine.api import urlfetch
import json
from facepy import GraphAPI
import handlers
import logging
import datetime
class PostFacebook(AuthHandler):
  def get(self, provider):
    if provider == "google":
        oauth_access_token = self.request.get("access_token")
        url = "https://www.googleapis.com/oauth2/v1/userinfo?access_token=%s" %oauth_access_token
        logging.info("theju %s"%url)
        result = urlfetch.fetch(url)
        if result.status_code == 200:
            d = json.loads(result.content)
            on_signin(self,d,'',provider)
    else:
        logging.info(self.request.headers.get('Cookie'))
        oauth_access_token = self.request.get("access_token")
        graph = GraphAPI(oauth_access_token)
        user_about_me = graph.get("/me")
        on_signin(self,user_about_me,'',provider)
    
class GetMyFriends(AuthHandler):
    def get(self):
        oauth_access_token = self.request.get("access_token")
        graph = GraphAPI(oauth_access_token)
        myfriends = graph.get("/me/friends")
        finalResult = {}
        allFriends = []
        for friend in myfriends['data']:
            auth_id = '%s:%s' % ('facebook', friend['id'])
            eachDict = {}
            eachDict['name'] = friend['name']
            eachDict['avatar'] = ''
            eachDict['issmashed'] = 'false'
            eachDict['id'] = friend['id']
            user = self.auth.store.user_model.get_by_auth_id(auth_id)
            if user:                
                eachDict['name'] = user.name
                eachDict['avatar'] = user.avatar_url
                eachDict['issmashed'] = 'true'
                eachDict['id'] = user.key.id()
            allFriends.append(eachDict)
        finalResult['friends'] = allFriends
        self.response.write(json.dumps(finalResult))         
def on_signin(self, data, auth_info, provider):
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
        self.auth.store.user_to_dict(user), remember=True)

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
          self.auth.set_session(self.auth.store.user_to_dict(user), remember=True)

    # Remember auth data during redirect, just for this demo. You wouldn't
    # normally do this.
    #self.session.add_flash(data, 'data - from _on_signin(...)')
    #self.session.add_flash(auth_info, 'auth_info - from _on_signin(...)')

    # Go to the profile page
    expires_date = datetime.datetime.utcnow() + datetime.timedelta(365)
    expires_str = expires_date.strftime("%d %b %Y %H:%M:%S GMT")
#    self.response.headers.add_header("Expires", expires_str)
    reviewsDict = {}
    #l_auth = self.auth.get_auth()
    userData = user#l_auth.store.user_model.get_by_id(userreview.userid)
    reviewsDict['username'] = userData.name
    reviewsDict['avatar'] = userData.avatar_url
    self.response.write(json.dumps(reviewsDict))
#    self.response.set_cookie('faceboologin', 'theju', expires=expires_date, path='/', domain='smashed.in')
#    self.response.write("<html><body>")
#    self.response.write("<p>Welcome to the Internet!</p>")
#    self.response.write("</body></html>")
