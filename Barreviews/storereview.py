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
import math

sys.path.append (os.path.join(os.path.abspath(os.path.dirname(__file__)), '../lib'))
from comments import CreateReview
from Cheetah.Template import Template
from User.handlers import AuthHandler
REVIEW_DB_NAME = 'bars_db'
def review_dbkey(review_dbname=REVIEW_DB_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('bars_db', review_dbname)

class ReviewDb(ndb.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    bid   = ndb.StringProperty()
    
    # icon_1 = ndb.BlobKeyProperty()
    # icon_2 = ndb.BlobKeyProperty()
    # icon_3 = ndb.BlobKeyProperty()
    # icon_4 = ndb.BlobKeyProperty()
    # icon_5 = ndb.BlobKeyProperty()
    # icon_6 = ndb.BlobKeyProperty()

    images = ndb.BlobKeyProperty (repeated=True)

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
    o_clean = ndb.StringProperty()
    o_bigscreen = ndb.StringProperty()
    latlon = ndb.GeoPtProperty()    
    reviewid = ndb.StringProperty()
    userid   = ndb.IntegerProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    
from skel.skel import Skel

class BRecordHandler (AuthHandler):
    def get(self):
        if not self.logged_in:
            self.session['redirect_url'] = '/b/record'
            self.redirect('/auth/')
        else:
            l_skel = Skel()
            l_skel.title = "Smashed.in :: Write a Review"

            #Head
            head_path = os.path.join (os.path.dirname (__file__), 'templates/upload-head.tmpl')
            l_skel.addtohead (str((Template.compile(file=head_path) (searchList={}))))

            #Body
            upload_url = blobstore.create_upload_url ('/api/b/upload')

            path = os.path.join (os.path.dirname (__file__), 'templates/upload-body.tmpl')
            template_values = {'upload_url': upload_url}
            l_skel.addtobody (str((Template.compile(file=path) (searchList=template_values))))

            self.response.out.write(l_skel.gethtml())    

def UpdateReviewRating(curRating,reviewId):
    review_query = ReviewDb.query(ReviewDb.reviewid == reviewId)		
    reviews = review_query.fetch(1)
    for review in reviews:
        existRating = float(review.rating)
        rating = float(curRating.strip())
        rating = (rating + existRating)/2
        rating = 0.5 * math.ceil(2.0 * rating)
        review.rating = '%s' %rating
        review.put()

class BSaveHandler (blobstore_handlers.BlobstoreUploadHandler, AuthHandler):
    def post(self):
        user_dict = self.auth.get_user_by_session()
        userId = user_dict['user_id']        
    
        review = ReviewDb(parent=review_dbkey(REVIEW_DB_NAME))
        review.bid = str(uuid.uuid4())

        #TODO: Validation min 1.
        icon1 = self.get_uploads('icon1')
        icon2 = self.get_uploads('icon2')
        icon3 = self.get_uploads('icon3')
        icon4 = self.get_uploads('icon4')
        icon5 = self.get_uploads('icon5')
        icon6 = self.get_uploads('icon6')

        review.images.append(icon1[0].key())
        review.images.append(icon2[0].key())
        review.images.append(icon3[0].key())
        review.images.append(icon4[0].key())
        review.images.append(icon5[0].key())
        review.images.append(icon6[0].key())
        
        review.name = self.request.get('name')
        review.address = self.request.get('address')
        review.phone = self.request.get('phone')
        rating = float(self.request.get('rating'))
        rating = 0.5 * math.ceil(2.0 * rating)
        review.rating = '%s' %rating
        review.description = self.request.get('description')
    
        review.snack_1 = self.request.get('favsnack1')
        review.snack_2 = self.request.get('favsnack2')
        review.snack_3 = self.request.get('favsnack3')
        review.snack_4 = self.request.get('favsnack4')
        
        review.usp1 = self.request.get('usp1')
        review.usp2 = self.request.get('usp2')
        review.o_bottlerate = self.request.get('bottlerate')
        review.o_smoke = self.request.get('smokingontable')
        review.o_budget = self.request.get('budget')
        review.o_musicvideo = self.request.get('music')    
        review.o_ac = self.request.get('ac')
        review.o_clean = self.request.get('clean')
        review.o_carpark = self.request.get('carpark')
        review.o_happyhours = self.request.get('happyhours')
        review.o_ladyok = self.request.get('ladyfriendly')
        review.o_cardaccept = self.request.get('cardaccepted')
        review.o_fightscene = self.request.get('fightscene')
        review.o_events = self.request.get('events')
        review.o_bigscreen = self.request.get('bigscreen')
        review.o_clean = self.request.get('clean')
        review.reviewid = CreateReview(self.request, 'init', userId)
        #review.latlon = ndb.GeoPtProperty()    
        review.put()

        self.redirect('/b/%s' % review.bid)

    
# application = webapp2.WSGIApplication([
#     ('/reviews/store/uploadreview', MainPageStore),
#     ('/reviews/store/upload', UploadHandler),
# ], debug=True)
