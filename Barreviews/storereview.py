import webapp2

import uuid
import cgi
import urllib

import os
import sys
from google.appengine.api import users

from google.appengine.ext import ndb

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

sys.path.append (os.path.join(os.path.abspath(os.path.dirname(__file__)), '../lib'))

from Cheetah.Template import Template

REVIEW_DB_NAME = 'bars_db'
def review_dbkey(review_dbname=REVIEW_DB_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('bars_db', review_dbname)

class ReviewDb(ndb.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    bid   = ndb.StringProperty()
    icon_1 = ndb.BlobKeyProperty()
    icon_2 = ndb.BlobKeyProperty()
    icon_3 = ndb.BlobKeyProperty()
    icon_4 = ndb.BlobKeyProperty()
    icon_5 = ndb.BlobKeyProperty()
    icon_6 = ndb.BlobKeyProperty()
    name = ndb.StringProperty()
    address = ndb.StringProperty()
    phone  = ndb.StringProperty()
    rating = ndb.StringProperty()
    description = ndb.PickleProperty()
    snack_1 = ndb.StringProperty()
    snack_2 = ndb.StringProperty()
    snack_3 = ndb.StringProperty()
    snack_4 = ndb.StringProperty()
    
    usp1 = ndb.StringProperty()
    usp2 = ndb.StringProperty()
    o_bottlerate = ndb.StringProperty()
    o_smoke = ndb.StringProperty()
    o_budget = ndb.StringProperty()
    o_musicvideo = ndb.StringProperty()    
    o_ac = ndb.StringProperty()
    o_clean = ndb.StringProperty()
    o_carpark = ndb.StringProperty()
    o_happyhours = ndb.StringProperty()
    o_ladyok = ndb.StringProperty()
    o_cardaccept = ndb.StringProperty()
    o_fightscene = ndb.StringProperty()
    o_events = ndb.StringProperty()
    
    latlon = ndb.GeoPtProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
  
class MainPageStore(webapp2.RequestHandler):

    def get(self):
        upload_url = blobstore.create_upload_url ('/reviews/store/upload')
        path = os.path.join (os.path.dirname (__file__), 'views/upload.html')
        #sign_query_params = urllib.urlencode ({'meme_db': MEME_DB_NAME})

        template_values = {'upload_url': upload_url}
        tmpl = Template( file = path, searchList = (template_values,) )

        self.response.write (tmpl)
        
class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
  def post(self):
    review = ReviewDb(parent=review_dbkey(REVIEW_DB_NAME))
    review.bid = str(uuid.uuid4())
    icon1 = self.get_uploads('icon1')
    review.icon_1 = icon1[0].key()
    icon2 = self.get_uploads('icon2')
    review.icon_2 = icon2[0].key()
    icon3 = self.get_uploads('icon3')
    review.icon_3 = icon3[0].key()
    icon4 = self.get_uploads('icon4')
    review.icon_4 = icon4[0].key()
    icon5 = self.get_uploads('icon5')
    review.icon_5 = icon5[0].key()
    icon6 = self.get_uploads('icon6')
    review.icon_6 = icon6[0].key()
    
    review.name = self.request.get('name')    
    review.address = self.request.get('address')
    review.phone = self.request.get('phone')
    review.rating = self.request.get('rating')
    review.description = self.request.get('description')

    review.snack_1 = self.request.get('snack1')
    review.snack_2 = self.request.get('snack2')
    review.snack_3 = self.request.get('snack3')
    review.snack_4 = self.request.get('snack4')
    
    review.usp1 = self.request.get('usp1')
    review.usp2 = self.request.get('usp2')
    review.o_bottlerate = self.request.get('bottlerate')
    review.o_smoke = self.request.get('smoke')
    review.o_budget = self.request.get('budget')
    review.o_musicvideo = self.request.get('musicvideo')    
    review.o_ac = self.request.get('ac')
    review.o_clean = self.request.get('clean')
    review.o_carpark = self.request.get('carpark')
    review.o_happyhours = self.request.get('happyhours')
    review.o_ladyok = self.request.get('ladyok')
    review.o_cardaccept = self.request.get('cardaccept')
    review.o_fightscene = self.request.get('fightscene')
    review.o_events = self.request.get('events')
    
    #review.latlon = ndb.GeoPtProperty()    
    review.put()
    self.redirect('/reviews/store/uploadreview')

    
# application = webapp2.WSGIApplication([
#     ('/reviews/store/uploadreview', MainPageStore),
#     ('/reviews/store/upload', UploadHandler),
# ], debug=True)
