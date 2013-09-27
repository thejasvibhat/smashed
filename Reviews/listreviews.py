import webapp2
from google.appengine.api import search
from google.appengine.ext import ndb
from review import ReviewDb
REVIEW_DB_NAME = 'bars_db'
class ListScenesHandler(webapp2.RequestHandler):
    def get(self):
        review_query = ReviewDb.query(ancestor=ndb.Key('bars_db',REVIEW_DB_NAME)).order(-ReviewDb.date)
        reviews = review_query.fetch(10)
            
        self.response.write('<reviews>');
        for review in reviews:
            self.response.write('<review>')
            self.response.write('<icon>')
            self.response.write('/download/review/file/1?bid=%s' %review.bid)
            self.response.write('</icon>')
            self.response.write('<url>')
            self.response.write('/reviews/scenes/%s' % review.bid)
            self.response.write('</url>')
            self.response.write('</review>')
        self.response.write('</reviews>')

class SearchHandler(webapp2.RequestHandler):
    def get(self):
        index = search.Index("name = prasanna")