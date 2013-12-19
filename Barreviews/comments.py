import webapp2

import uuid
import cgi
import urllib
from webapp2_extras import auth, sessions
import os
from google.appengine.api import users

from google.appengine.ext import ndb

import storereview

from User.handlers import AuthHandler

REVIEW_DB_NAME = 'bars_db_review'
def review_dbkey(review_dbname=REVIEW_DB_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('bars_db_review', review_dbname) 


class CommentReviewDb(ndb.Model):
    userid = ndb.IntegerProperty()
    reviewid = ndb.StringProperty()
    parentid = ndb.StringProperty()
    review = ndb.StringProperty()
    rating = ndb.StringProperty()
    snack1 = ndb.StringProperty()
    snack2 = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    

    
def CreateReview (reviewDict,parentid,userid):
    review = CommentReviewDb(parent=review_dbkey(REVIEW_DB_NAME))
    review.userid = userid
    review.reviewid = str(uuid.uuid4())
    if parentid == 'init':
        review.parentid = review.reviewid
    else:
        review.parentid = parentid
    review.review = reviewDict.get('description')
    review.rating = reviewDict.get('rating')
    review.snack1 = reviewDict.get('favsnack1')
    review.snack2 = reviewDict.get('favsnack2')
    review.put()
    return str(review.reviewid)
        
class UpdateComment (AuthHandler):
    def get(self):
        reviewid = self.request.get('reviewid')
        comment = self.request.get('review')
        rating = self.request.get('rating')
        storereview.UpdateReviewRating(rating,reviewid)
        review_query = CommentReviewDb.query(CommentReviewDb.reviewid == reviewid)		
        reviews = review_query.fetch(1)
        for review in reviews:
            review.rating = rating
            review.review = comment
            review.put()
        self.response.write('%s' %reviewid)     
    
class AddComment (AuthHandler):
    def get(self):
        commentid = CreateReview(self.request, self.request.get('reviewid'), self.user_id)
        storereview.UpdateReviewRating(self.request.get('rating'),self.request.get('reviewid'))
        self.response.write('%s' %commentid)     
        
