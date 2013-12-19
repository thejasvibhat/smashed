import webapp2
import sys
import os
import logging
from google.appengine.ext import ndb
from storereview import ReviewDb
from comments import CommentReviewDb
from address import LocationDb
from webapp2_extras import auth, sessions
import math
import json
from User.handlers import AuthHandler
sys.path.append (os.path.join(os.path.abspath(os.path.dirname(__file__)), '../lib'))

from Cheetah.Template import Template

from skel.skel import Skel


REVIEW_DB_NAME = 'bars_db'
def review_dbkey(review_dbname=REVIEW_DB_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('bars_db', review_dbname) 


class ReviewHandler(AuthHandler):
    def get(self,pagenum=1):
        pagenum = int(pagenum)
        items_per_page = 12
        offset = 0
        if pagenum != 1:
            offset = (pagenum * items_per_page) - 1
 
        l_skel = Skel()
	l_skel.title = "Smashed.in :: Latest Additions"
        #Head
        head_path = os.path.join (os.path.dirname (__file__), 'templates/reviews-head.tmpl')
        l_skel.addtohead (str((Template.compile(file=head_path) (searchList={}))))

        #Body
        review_query = ReviewDb.query(ancestor=review_dbkey(REVIEW_DB_NAME)).order(-ReviewDb.date)
        reviews = review_query.fetch()
        for review in reviews[offset:offset+items_per_page]:
            addressid = str(review.addressid)
            add_querry = LocationDb.query(LocationDb.addressid == addressid)
            addresses = add_querry.fetch()
            for addressLoc in addresses:
                review.latlon = '%s:%s' %(addressLoc.lat,addressLoc.lng)
        
        template_values = {
		"reviews" : reviews[offset:offset+items_per_page],
		"currentpage" : pagenum,
		"userid": self.user_id,
		"totalpagecount" : math.ceil (len(reviews) / items_per_page)
	}
        path = os.path.join (os.path.dirname (__file__), 'templates/reviews-body.tmpl')
        l_skel.addtobody (str((Template.compile(file=path) (searchList=template_values))))

        self.response.out.write(l_skel.gethtml())

class SceneHandler(AuthHandler):
    def get(self, resource, name=None):
        l_skel = Skel()
        bid = resource 
        head_path = os.path.join (os.path.dirname (__file__), 'templates/b-head.tmpl')
        l_skel.addtohead (str((Template.compile(file=head_path) (searchList={}))))

        c = {}
        review_query = ReviewDb.query(ReviewDb.bid == bid)
        reviews = review_query.fetch(1)

        for review in reviews:
            if review.bid == bid:
                revid = str(review.reviewid)
                userreview_querry = CommentReviewDb.query(CommentReviewDb.parentid == revid)
                userreviews = userreview_querry.fetch()
                userDetails = self.current_user
                c['currentuser'] = userDetails
                rating = 0
                totalReviews = 0
                allReviewsDict = []
                for userreview in userreviews:
                    rating += float(userreview.rating.strip())

                    l_auth = auth.get_auth()
                    userData = l_auth.store.user_model.get_by_id(userreview.userid)
                    reviewsDict = {}
                    reviewsDict['rating'] = userreview.rating
                    reviewsDict['review'] = userreview.review
                    reviewsDict['username'] = userData.name
                    reviewsDict['avatar'] = userData.avatar_url
                    allReviewsDict.append(reviewsDict)
                    totalReviews = totalReviews + 1                    
                logging.info(reviewsDict)
                rating = rating/totalReviews
                rating = 0.5 * math.ceil(2.0 * rating)
                c['rating'] = '%s' %rating
                addressid = str(review.addressid)
                add_querry = LocationDb.query(LocationDb.addressid == addressid)
                addresses = add_querry.fetch()
                for addressLoc in addresses:
                    c['lat'] = '%s' %addressLoc.lat
                    #c['lon'] = '%s' % review.latlon.lon
                    c['lon'] = '%s' %addressLoc.lng
                    add = "<br />".join(addressLoc.formattedaddress.split("\n"))                
                    c['address'] = '%s' % add                    
                c['reviewlist'] = allReviewsDict
                #12.913762,77.600119                
                c['name'] = '%s' % review.name
                #c['lat'] = '%s' % review.latlon.lat
                c['phone'] ='%s' % review.phone
                desc = "<br />".join(userreviews[0].review.split("\n"))
                c['description'] = '%s' %desc
                c['reviewid'] = '%s' %review.reviewid

                c['images'] = review.images
                
                
				
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
                c['snack1'] = '%s' %userreviews[0].snack1
                c['snack2'] = '%s' %userreviews[0].snack2				
				
                c['usp1'] = "Bottle Rate"
                c['usp2'] = "Lady Friendly"
                
        path = os.path.join (os.path.dirname (__file__), 'templates/b-body.tmpl')
        l_skel.addtobody (str((Template.compile(file=path) (searchList=c))))

        l_skel.title = "Smashed.in :: %s" % review.name
        self.response.out.write(l_skel.gethtml())


    
# application = webapp2.WSGIApplication([
#     ('/reviews/scenes/listscenes', ListScenesHandler),
#     ('/reviews/scenes/search', SearchHandler),
#     ('/reviews/scenes/([^/]+)?', SceneHandler),    
# ], debug=True)
