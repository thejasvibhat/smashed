
#some stackoverflow link.

from google.appengine.ext import ndb
from webapp2_extras.appengine.auth.models import User as Webapp2User

class User(Webapp2User):
    usertype = ndb.StringProperty (repeated=True)
