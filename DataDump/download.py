import webapp2
import logging
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

class GetRes (blobstore_handlers.BlobstoreDownloadHandler):
  def get (self, resource):
      blob_info = blobstore.BlobInfo.get(resource)
      self.send_blob(blob_info)

class GetIcon (blobstore_handlers.BlobstoreDownloadHandler):
  def get (self, resource):
      blob_info = blobstore.BlobInfo.get(resource)
      self.send_blob(blob_info)

class GetFile(blobstore_handlers.BlobstoreDownloadHandler):
  def get(self):
        myId=self.request.get('id')        
        meme_query = MemeDb.query(MemeDb.myid == myId)
        memes = meme_query.fetch(1)

        for meme in memes:
            if meme.myid == myId:
                    blob_info = blobstore.BlobInfo.get(meme.resid)
                    self.send_blob(blob_info)

# application = webapp2.WSGIApplication([
#     ('/download/meme/icon',GetIcon),
#     ('/download/meme/file',GetFile),
#     ('/download/review/icon/([^/]+)?',GetIconReview),
#     ('/download/review/file/([^/]+)?',GetFileReview),    
# ], debug=True)
