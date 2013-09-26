import webapp2

import os

from google.appengine.ext import ndb

from Reviews.storereview import ReviewDb

import jinja2
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])


REVIEW_DB_NAME = 'bars_db'
def review_dbkey(review_dbname=REVIEW_DB_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('bars_db', review_dbname) 




class SceneHandler(webapp2.RequestHandler):
    def get(self, resource):
        bid = resource 
        t = JINJA_ENVIRONMENT.get_template('views/index.html')
        c = {}
        review_query = ReviewDb.query(ancestor=review_dbkey(REVIEW_DB_NAME)).order(-ReviewDb.date)
        reviews = review_query.fetch(10)


        for review in reviews:
            if review.bid == bid:
                c['description'] = '%s' %review.description
                c['name'] = '%s' % review.name
                add = "<br />".join(review.address.split("\n"))                
                c['address'] = '%s' % add
                c['phone'] ='%s' % review.phone                
                c['icon1'] = '/download/review/file/1?bid=%s' %review.bid
                c['icon2'] = '/download/review/file/2?bid=%s' %review.bid
                c['icon3'] = '/download/review/file/3?bid=%s' %review.bid
                c['icon4'] = '/download/review/file/4?bid=%s' %review.bid
                c['icon5'] = '/download/review/file/5?bid=%s' %review.bid
                c['icon6'] = '/download/review/file/6?bid=%s' %review.bid
                
        self.response.write(t.render(c))
    
application = webapp2.WSGIApplication([
    ('/reviews/scenes/([^/]+)?', SceneHandler),
], debug=True)
