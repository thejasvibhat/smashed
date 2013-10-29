import webapp2
from google.appengine.api import search
from google.appengine.ext import ndb
from review import ReviewDb
REVIEW_DB_NAME = 'bars_db'
class ListScenesHandler(webapp2.RequestHandler):
    def get(self):
        review_query = ReviewDb.query(ancestor=ndb.Key('bars_db',REVIEW_DB_NAME)).order(-ReviewDb.date)
        oLimit = int(self.request.get("limit"))
        oOffset = int(self.request.get("offset"))
        reviews = review_query.fetch(oLimit,offset=oOffset)
        self.response.write('<reviews>')
        for review in reviews:
            self.response.write('<review>')
            self.response.write('<name>')
            self.response.write('%s' %review.name)
            self.response.write('</name>')
			
			
            self.response.write('<icon1>')
            self.response.write('/download/review/file/1?bid=%s' %review.bid)
            self.response.write('</icon1>')
			
            self.response.write('<icon2>')
            self.response.write('/download/review/file/2?bid=%s' %review.bid)
            self.response.write('</icon2>')

            self.response.write('<icon3>')
            self.response.write('/download/review/file/3?bid=%s' %review.bid)
            self.response.write('</icon3>')

            self.response.write('<icon4>')
            self.response.write('/download/review/file/4?bid=%s' %review.bid)
            self.response.write('</icon4>')

            self.response.write('<icon5>')
            self.response.write('/download/review/file/5?bid=%s' %review.bid)
            self.response.write('</icon5>')

            self.response.write('<icon6>')
            self.response.write('/download/review/file/6?bid=%s' %review.bid)
            self.response.write('</icon6>')
			
            self.response.write('<url>')
            self.response.write('/reviews/scenes/%s' % review.bid)
            self.response.write('</url>')
            self.response.write('</review>')
            self.response.write('</reviews>')

class SearchHandler(webapp2.RequestHandler):
    def get(self):
        index = search.Index("name = prasanna")