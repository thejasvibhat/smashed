import webapp2
import json
from google.appengine.api import search
from google.appengine.ext import ndb
from webapp2_extras import auth, sessions
from review import ReviewDb
from review import CommentReviewDb
from User.handlers import AuthHandler
from google.appengine.api import search
_INDEX_NAME = 'localityTagSearch'
REVIEW_DB_NAME = 'bars_db'

class RegionDb(ndb.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    city    = ndb.StringProperty()
    locality = ndb.StringProperty()
    pincode   = ndb.StringProperty()

class ListScenesHandler (webapp2.RequestHandler):
    def get(self):
        review_query = ReviewDb.query(ancestor=ndb.Key('bars_db',REVIEW_DB_NAME)).order(-ReviewDb.date)
        oLimit = int(self.request.get("limit", default_value="10"))
        oOffset = int(self.request.get("offset", default_value="0"))
        reviews = review_query.fetch(oLimit,offset=oOffset)
        self.response.write('<reviews>')
        for review in reviews:
            self.response.write('<review>')
            self.response.write('<name>')
            self.response.write('%s' %review.name)
            self.response.write('</name>')

            self.response.write('<icon>')
            self.response.write('/res/download/%s' % review.images[0])
            self.response.write('</icon>')

            self.response.write('<url>')
            self.response.write('/b/%s' % review.bid)
            self.response.write('</url>')
            self.response.write('</review>')
        self.response.write('</reviews>')
        self.response.headers['Content-Type'] = 'text/xml'

class ListComments(AuthHandler):
    def get (self):
        resource = self.request.get ("reviewid");
        revid = resource
        userreview_querry = CommentReviewDb.query(CommentReviewDb.parentid == revid).order(CommentReviewDb.date)
        oLimit = int(self.request.get("limit", default_value="10"))
        oOffset = int(self.request.get("offset", default_value="0"))
        userreviews = userreview_querry.fetch(oLimit,offset=oOffset)
        finalDict = {}
        reviewsDict = {}
        if self.logged_in:
            curuserdata = self.current_user             
            reviewsDict['username'] = curuserdata.name
            reviewsDict['avatar'] = curuserdata.avatar_url
            finalDict['curuser'] = reviewsDict
        
        allReviewsDict = []
        for userreview in userreviews:
            l_auth = auth.get_auth()
            userData = l_auth.store.user_model.get_by_id(userreview.userid)
            reviewsDict = {}
            if self.logged_in:
                curUserId = self.user_id
                if curUserId == userreview.userid:
                    reviewsDict['rating'] = userreview.rating
                    reviewsDict['review'] = userreview.review
                    reviewsDict['reviewid'] = userreview.reviewid
                    if userreview.parentid == userreview.reviewid:
                        reviewsDict['desreview'] = 1        
                    finalDict['curuserreview'] = reviewsDict
                else:
                    reviewsDict['rating'] = userreview.rating
                    reviewsDict['review'] = userreview.review
                    reviewsDict['username'] = userData.name
                    reviewsDict['avatar'] = userData.avatar_url
                    if userreview.parentid == userreview.reviewid:
                        reviewsDict['desreview'] = 1        
                    allReviewsDict.append(reviewsDict)                    
            else:
                reviewsDict['rating'] = userreview.rating
                reviewsDict['review'] = userreview.review
                reviewsDict['username'] = userData.name
                reviewsDict['avatar'] = userData.avatar_url
                if userreview.parentid == userreview.reviewid:
                    reviewsDict['desreview'] = 1        
                allReviewsDict.append(reviewsDict)
        
        finalDict['reviews'] = allReviewsDict
        self.response.write(json.dumps(finalDict))

class ListFsComments(AuthHandler):
    def get (self):
        resource = self.request.get ("fsbid");
        revid = resource
        userreview_querry = CommentReviewDb.query(CommentReviewDb.fsbid == revid).order(CommentReviewDb.date)
        oLimit = int(self.request.get("limit", default_value="10"))
        oOffset = int(self.request.get("offset", default_value="0"))
        userreviews = userreview_querry.fetch(oLimit,offset=oOffset)
        finalDict = {}
        reviewsDict = {}
        if self.logged_in:
            curuserdata = self.current_user             
            reviewsDict['username'] = curuserdata.name
            reviewsDict['avatar'] = curuserdata.avatar_url
            finalDict['curuser'] = reviewsDict
        
        allReviewsDict = []
        for userreview in userreviews:
            l_auth = auth.get_auth()
            userData = l_auth.store.user_model.get_by_id(userreview.userid)
            reviewsDict = {}
            if self.logged_in:
                curUserId = self.user_id
                if curUserId == userreview.userid:
                    reviewsDict['rating'] = userreview.rating
                    reviewsDict['review'] = userreview.review
                    reviewsDict['reviewid'] = userreview.reviewid
                    if userreview.parentid == userreview.reviewid:
                        reviewsDict['desreview'] = 1        
                    finalDict['curuserreview'] = reviewsDict
                else:
                    reviewsDict['rating'] = userreview.rating
                    reviewsDict['review'] = userreview.review
                    reviewsDict['username'] = userData.name
                    reviewsDict['avatar'] = userData.avatar_url
                    if userreview.parentid == userreview.reviewid:
                        reviewsDict['desreview'] = 1        
                    allReviewsDict.append(reviewsDict)                    
            else:
                reviewsDict['rating'] = userreview.rating
                reviewsDict['review'] = userreview.review
                reviewsDict['username'] = userData.name
                reviewsDict['avatar'] = userData.avatar_url
                if userreview.parentid == userreview.reviewid:
                    reviewsDict['desreview'] = 1        
                allReviewsDict.append(reviewsDict)
        
        finalDict['reviews'] = allReviewsDict
        self.response.write(json.dumps(finalDict))
class AjaxLocality(AuthHandler):
    def get (self):
        resource = self.request.get ("search");
        stype = self.request.get ("type");
        expr_list = [search.SortExpression(
            expression='tagsAddress', default_value='',
            direction=search.SortExpression.DESCENDING)]
        # construct the sort options
        sort_opts = search.SortOptions(
             expressions=expr_list)
        query_options = search.QueryOptions(
            limit=100,
            sort_options=sort_opts)
        if stype == 'bar':
            q = 'tagsName:%s'%resource
        else:
            q = 'tagsAddress:%s'%resource
        query_obj = search.Query(query_string=q, options=query_options)
        results = search.Index(name=_INDEX_NAME).search(query=query_obj)
        finalDict = {}
        allRegs = []
        for result in results:
            locRes = {}
            #locRes['name'] = '%s' %result.fields[3].value
            #locRes['locality'] = '%s' %result.fields[2].value
            locRes['label'] = '%s in %s' %(result.fields[3].value,result.fields[2].value)
            locRes['value'] = '%s' %result.fields[3].value
            locRes['bid'] = '%s' %result.fields[6].value
            allRegs.append(locRes)#'%s' %result.fields[2].value)
        finalDict['results'] = allRegs
        self.response.write(json.dumps(finalDict))
        
##        return
##        regQuerry = RegionDb.query(RegionDb.locality < resource)
##        regs = regQuerry.fetch(15)
##        finalDict = {}
##        allRegs = []
##        for reg in regs:            
##            allRegs.append('%s' %reg.locality)
##        finalDict['results'] = allRegs
##        self.response.write(json.dumps(finalDict))
        
class SearchHandler(webapp2.RequestHandler):
    def get(self):
        index = search.Index("name = prasanna")

