import webapp2
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import ndb
from MemeCreator.meme import MemeDb
from Barreviews.review import ReviewDb
MEME_DB_NAME = 'meme_db'
REVIEW_DB_NAME = 'bars_db'
def dbkey(dbname):
    return ndb.Key(dbname,dbname)

class GetFile(blobstore_handlers.BlobstoreDownloadHandler):
  def get(self):
        myId=self.request.get('id')        
        meme_query = MemeDb.query(ancestor=dbkey(MEME_DB_NAME)).order(-MemeDb.date)
        memes = meme_query.fetch(10)


        for meme in memes:
            if meme.myid == myId:
                    blob_info = blobstore.BlobInfo.get(meme.resid)
                    self.send_blob(blob_info)

class GetIcon(webapp2.RequestHandler):

    def get(self):
        myId=self.request.get('id')        
        meme_query = MemeDb.query(ancestor=dbkey(MEME_DB_NAME)).order(-MemeDb.date)
        memes = meme_query.fetch(10)


        for meme in memes:
            if meme.myid == myId:
                self.response.write('%s' %
                                meme.icon)


class GetFileReview(blobstore_handlers.BlobstoreDownloadHandler):
  def get(self,resource):
        bid=self.request.get('bid')        
        review_query = ReviewDb.query(ancestor=dbkey(REVIEW_DB_NAME)).order(-ReviewDb.date)
        reviews = review_query.fetch(10)


        for review in reviews:
            if review.bid == bid:
                if resource == '1':
                    blob_info = blobstore.BlobInfo.get(review.icon_1)
                elif resource == '2':
                    blob_info = blobstore.BlobInfo.get(review.icon_2)
                elif resource == '3':
                    blob_info = blobstore.BlobInfo.get(review.icon_3)
                elif resource == '4':
                    blob_info = blobstore.BlobInfo.get(review.icon_4)
                elif resource == '5':
                    blob_info = blobstore.BlobInfo.get(review.icon_5)
                elif resource == '6':
                    blob_info = blobstore.BlobInfo.get(review.icon_6)                    
                self.send_blob(blob_info)

class GetIconReview(webapp2.RequestHandler):

    def get(self,resource):
        bid=self.request.get('bid')        
        review_query = ReviewDb.query(ancestor=dbkey(REVIEW_DB_NAME)).order(-ReviewDb.date)
        reviews = review_query.fetch(10)


        for review in reviews:
            if review.bid == bid:
                if resource == 1:
                    blob_info = blobstore.BlobInfo.get(review.icon_1)
                elif resource == 2:
                    blob_info = blobstore.BlobInfo.get(review.icon_2)
                elif resource == 3:
                    blob_info = blobstore.BlobInfo.get(review.icon_3)
                elif resource == 4:
                    blob_info = blobstore.BlobInfo.get(review.icon_4)
                elif resource == 5:
                    blob_info = blobstore.BlobInfo.get(review.icon_5)
                elif resource == 6:
                    blob_info = blobstore.BlobInfo.get(review.icon_6)                    
                self.send_blob(blob_info)



# application = webapp2.WSGIApplication([
#     ('/download/meme/icon',GetIcon),
#     ('/download/meme/file',GetFile),
#     ('/download/review/icon/([^/]+)?',GetIconReview),
#     ('/download/review/file/([^/]+)?',GetFileReview),    
# ], debug=True)
