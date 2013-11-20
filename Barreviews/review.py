import webapp2
import sys
import os
import logging
from google.appengine.ext import ndb
from storereview import ReviewDb
sys.path.append (os.path.join(os.path.abspath(os.path.dirname(__file__)), '../lib'))
import jinja2
from Cheetah.Template import Template

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

REVIEW_DB_NAME = 'bars_db'
def review_dbkey(review_dbname=REVIEW_DB_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('bars_db', review_dbname) 


class ReviewHandler(webapp2.RequestHandler):
    def get(self):
        path = os.path.join (os.path.dirname (__file__), 'views/reviews.html')
        review_query = ReviewDb.query(ancestor=review_dbkey(REVIEW_DB_NAME)).order(-ReviewDb.date)
        reviews = review_query.fetch(12)

        id = 0;
        template_values = {}
        for review in reviews:
            id = id + 1
            ratingUrl = ''
            if review.rating == "1":
			    ratingUrl = '/reviewhtml/assets/rate_1.png'
            if review.rating == "1.5":
			    ratingUrl = '/reviewhtml/assets/rate_1_5.png'
            if review.rating == "2":
			    ratingUrl = '/reviewhtml/assets/rate_2.png'
            if review.rating == "2.5":
			    ratingUrl = '/reviewhtml/assets/rate_2_5.png'
            if review.rating == "3":
			    ratingUrl = '/reviewhtml/assets/rate_3.png'
            if review.rating == "3.5":
		        ratingUrl = '/reviewhtml/assets/rate_3_5.png'
            if review.rating == "4":
			    ratingUrl = '/reviewhtml/assets/rate_4.png'
            if review.rating == "4.5":
			    ratingUrl = '/reviewhtml/assets/rate_4_5.png'
            if review.rating == "5":
			    ratingUrl = '/reviewhtml/assets/rate_5.png'
            add = "<br />".join(review.address.split("\n"))                
            template_values['name%s'%id] = '%s'%review.name
            template_values['rating%s'%id] = '%s'%ratingUrl
            template_values['address%s'%id] = '%s'%add
            template_values['image%s'%id] = '/download/review/file/1?bid=%s' %review.bid			
            template_values['url%s'%id] = '/reviews/scenes/%s' %review.bid						
        logging.info('%s' %template_values)
        tclass = Template.compile (file = path)
        t = tclass(searchList=template_values)
        self.response.out.write(t)
		
class SceneHandler(webapp2.RequestHandler):
    def get(self, resource):
        bid = resource 
        t = JINJA_ENVIRONMENT.get_template('index.html')
        c = {}
        review_query = ReviewDb.query(ReviewDb.bid == bid)		
        reviews = review_query.fetch(1)

        for review in reviews:
            if review.bid == bid:
                #12.913762,77.600119                
                c['name'] = '%s' % review.name
                #c['lat'] = '%s' % review.latlon.lat
                c['lat'] = '12.913762'
                #c['lon'] = '%s' % review.latlon.lon
                c['lon'] = '77.600119'
                add = "<br />".join(review.address.split("\n"))                
                c['address'] = '%s' % add
                c['phone'] ='%s' % review.phone
                desc = "<br />".join(review.description.split("\n"))
                c['description'] = '%s' %desc               
                c['icon1'] = '/download/review/file/1?bid=%s' %review.bid
                c['icon2'] = '/download/review/file/2?bid=%s' %review.bid
                c['icon3'] = '/download/review/file/3?bid=%s' %review.bid
                c['icon4'] = '/download/review/file/4?bid=%s' %review.bid
                c['icon5'] = '/download/review/file/5?bid=%s' %review.bid
                c['icon6'] = '/download/review/file/6?bid=%s' %review.bid
                c['rating'] = '%s' %review.rating
				
                c['budget'] = '%s' %review.o_budget
                c['ac'] = '%s' %review.o_ac
                c['carpark'] = '%s' %review.o_carpark
                c['bigscreen'] = '%s' %review.o_bigscreen
                c['ladyok'] = '%s' %review.o_ladyok
                c['fightscene'] = '%s' %review.o_fightscene
                c['musicvideo'] = '%s' %review.o_musicvideo
                c['clean'] = '%s' %review.o_clean
                c['smoke'] = '%s' %review.o_smoke
                c['happyhours'] = '%s' %review.o_happyhours
                c['check_card'] = '%s' %review.o_cardaccept
                c['events'] = '%s' %review.o_events
                c['bottlerate'] = '%s' %review.o_bottlerate
                c['snack1'] = '%s' %review.snack_1
                c['snack2'] = '%s' %review.snack_2				
				
                c['usp1'] = "Bottle Rate"
                c['usp2'] = "Lady Friendly"
                
        self.response.write(t.render(c))
    
# application = webapp2.WSGIApplication([
#     ('/reviews/scenes/listscenes', ListScenesHandler),
#     ('/reviews/scenes/search', SearchHandler),
#     ('/reviews/scenes/([^/]+)?', SceneHandler),    
# ], debug=True)
